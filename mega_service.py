"""
Serviço para integração com a MEGA API
"""
import os
import tempfile
import uuid
from mega import Mega
from src.models.mega_account import MegaAccount, db
from src.utils.encryption import decrypt_password
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MegaService:
    def __init__(self):
        self.mega_clients = {}  # Cache de clientes autenticados
    
    def get_mega_client(self, account_id):
        """Obter cliente MEGA autenticado para uma conta específica"""
        if account_id in self.mega_clients:
            return self.mega_clients[account_id]
        
        account = MegaAccount.query.get(account_id)
        if not account or not account.is_active:
            raise Exception(f"Conta MEGA {account_id} não encontrada ou inativa")
        
        try:
            # Desencriptar palavra-passe
            password = decrypt_password(account.password)
            
            # Criar cliente MEGA
            mega = Mega()
            mega_client = mega.login(account.email, password)
            
            # Cache do cliente
            self.mega_clients[account_id] = mega_client
            
            logger.info(f"Cliente MEGA autenticado para conta {account.email}")
            return mega_client
            
        except Exception as e:
            logger.error(f"Erro ao autenticar conta MEGA {account.email}: {str(e)}")
            raise Exception(f"Falha na autenticação da conta MEGA: {str(e)}")
    
    def get_best_account_for_upload(self, file_size):
        """Encontrar a melhor conta MEGA para upload baseada no espaço disponível"""
        accounts = MegaAccount.query.filter_by(is_active=True).all()
        
        if not accounts:
            raise Exception("Nenhuma conta MEGA ativa disponível")
        
        # Filtrar contas com espaço suficiente
        suitable_accounts = []
        for account in accounts:
            available_space = account.total_space - account.used_space
            if available_space >= file_size:
                suitable_accounts.append((account, available_space))
        
        if not suitable_accounts:
            raise Exception("Nenhuma conta MEGA tem espaço suficiente para este ficheiro")
        
        # Ordenar por espaço disponível (maior primeiro)
        suitable_accounts.sort(key=lambda x: x[1], reverse=True)
        
        return suitable_accounts[0][0]
    
    def upload_file(self, file_data, filename, category, file_size):
        """Upload de ficheiro para MEGA"""
        try:
            # Encontrar melhor conta para upload
            account = self.get_best_account_for_upload(file_size)
            
            # Obter cliente MEGA
            mega_client = self.get_mega_client(account.id)
            
            # Gerar nome único para o ficheiro
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Criar ficheiro temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
                # Escrever dados do ficheiro
                if hasattr(file_data, 'read'):
                    # Se for um objeto file-like
                    file_data.seek(0)
                    temp_file.write(file_data.read())
                else:
                    # Se for bytes
                    temp_file.write(file_data)
                
                temp_file_path = temp_file.name
            
            try:
                # Upload para MEGA
                mega_file = mega_client.upload(temp_file_path, dest_filename=unique_filename)
                
                # Obter link de partilha
                share_link = mega_client.get_upload_link(mega_file)
                
                # Obter ID do ficheiro no MEGA
                mega_file_id = mega_file
                
                # Atualizar espaço usado da conta
                account.used_space += file_size
                account.last_updated = datetime.utcnow()
                db.session.commit()
                
                logger.info(f"Ficheiro {filename} carregado com sucesso para conta {account.email}")
                
                return {
                    'mega_account_id': account.id,
                    'mega_file_id': str(mega_file_id),
                    'mega_filename': unique_filename,
                    'share_link': share_link
                }
                
            finally:
                # Limpar ficheiro temporário
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Erro no upload para MEGA: {str(e)}")
            raise Exception(f"Falha no upload: {str(e)}")
    
    def delete_file(self, mega_file_id, account_id):
        """Eliminar ficheiro do MEGA"""
        try:
            mega_client = self.get_mega_client(account_id)
            
            # Eliminar ficheiro
            mega_client.delete(mega_file_id)
            
            logger.info(f"Ficheiro {mega_file_id} eliminado da conta {account_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao eliminar ficheiro do MEGA: {str(e)}")
            raise Exception(f"Falha na eliminação: {str(e)}")
    
    def update_account_space(self, account_id):
        """Atualizar informações de espaço de uma conta MEGA"""
        try:
            account = MegaAccount.query.get(account_id)
            if not account:
                raise Exception("Conta não encontrada")
            
            mega_client = self.get_mega_client(account_id)
            
            # Obter informações de quota
            quota_info = mega_client.get_quota()
            
            # Atualizar na base de dados
            account.total_space = quota_info['total']
            account.used_space = quota_info['used']
            account.last_updated = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Espaço atualizado para conta {account.email}: {quota_info['used']}/{quota_info['total']}")
            
            return {
                'total_space': quota_info['total'],
                'used_space': quota_info['used'],
                'available_space': quota_info['total'] - quota_info['used']
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar espaço da conta: {str(e)}")
            raise Exception(f"Falha na atualização: {str(e)}")
    
    def test_account_connection(self, email, password):
        """Testar conexão com uma conta MEGA"""
        try:
            mega = Mega()
            mega_client = mega.login(email, password)
            
            # Obter informações básicas para verificar se a conexão funciona
            quota_info = mega_client.get_quota()
            
            return {
                'success': True,
                'total_space': quota_info['total'],
                'used_space': quota_info['used']
            }
            
        except Exception as e:
            logger.error(f"Erro ao testar conta MEGA {email}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_account_files(self, account_id):
        """Obter lista de ficheiros de uma conta MEGA"""
        try:
            mega_client = self.get_mega_client(account_id)
            
            # Obter ficheiros
            files = mega_client.get_files()
            
            file_list = []
            for file_id, file_info in files.items():
                if file_info['t'] == 0:  # Apenas ficheiros (não pastas)
                    file_list.append({
                        'id': file_id,
                        'name': file_info['a']['n'] if 'a' in file_info and 'n' in file_info['a'] else 'Unknown',
                        'size': file_info['s'],
                        'created': file_info.get('ts', 0)
                    })
            
            return file_list
            
        except Exception as e:
            logger.error(f"Erro ao obter ficheiros da conta: {str(e)}")
            raise Exception(f"Falha ao obter ficheiros: {str(e)}")
    
    def clear_client_cache(self, account_id=None):
        """Limpar cache de clientes MEGA"""
        if account_id:
            self.mega_clients.pop(account_id, None)
        else:
            self.mega_clients.clear()
        
        logger.info("Cache de clientes MEGA limpo")

# Instância global do serviço
mega_service = MegaService()

