"""
Serviço simulado para integração com a MEGA API (para demonstração)
NOTA: Para produção, usar Python 3.8 ou 3.9 com mega.py real
"""
import os
import uuid
import time
import random
from src.models.mega_account import MegaAccount, db
from src.utils.encryption import decrypt_password
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MegaServiceMock:
    def __init__(self):
        self.mock_files = {}  # Simular armazenamento de ficheiros
    
    def get_mega_client(self, account_id):
        """Simular cliente MEGA autenticado"""
        account = MegaAccount.query.get(account_id)
        if not account or not account.is_active:
            raise Exception(f"Conta MEGA {account_id} não encontrada ou inativa")
        
        logger.info(f"Cliente MEGA simulado para conta {account.email}")
        return f"mock_client_{account_id}"
    
    def get_best_account_for_upload(self, file_size):
        """Encontrar a melhor conta MEGA para upload (simulado)"""
        accounts = MegaAccount.query.filter_by(is_active=True).all()
        
        if not accounts:
            raise Exception("Nenhuma conta MEGA ativa disponível")
        
        # Simular seleção da melhor conta
        suitable_accounts = []
        for account in accounts:
            available_space = account.total_space - account.used_space
            if available_space >= file_size:
                suitable_accounts.append((account, available_space))
        
        if not suitable_accounts:
            # Se não há contas com espaço, criar uma conta simulada
            mock_account = MegaAccount(
                email="mock@mega.nz",
                password="encrypted_mock_password",
                total_space=50 * 1024 * 1024 * 1024,  # 50GB
                used_space=0,
                is_active=True
            )
            db.session.add(mock_account)
            db.session.commit()
            return mock_account
        
        # Ordenar por espaço disponível (maior primeiro)
        suitable_accounts.sort(key=lambda x: x[1], reverse=True)
        return suitable_accounts[0][0]
    
    def upload_file(self, file_data, filename, category, file_size):
        """Simular upload de ficheiro para MEGA"""
        try:
            # Simular tempo de upload
            time.sleep(0.5)
            
            # Encontrar melhor conta para upload
            account = self.get_best_account_for_upload(file_size)
            
            # Gerar dados simulados
            unique_filename = f"{uuid.uuid4()}_{filename}"
            mock_file_id = f"mock_file_{uuid.uuid4()}"
            mock_share_link = f"https://mega.nz/file/{uuid.uuid4().hex[:8]}#{uuid.uuid4().hex[:22]}"
            
            # Simular armazenamento
            self.mock_files[mock_file_id] = {
                'filename': unique_filename,
                'size': file_size,
                'account_id': account.id,
                'upload_date': datetime.utcnow()
            }
            
            # Atualizar espaço usado da conta
            account.used_space += file_size
            account.last_updated = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Ficheiro {filename} simulado com sucesso para conta {account.email}")
            
            return {
                'mega_account_id': account.id,
                'mega_file_id': mock_file_id,
                'mega_filename': unique_filename,
                'share_link': mock_share_link
            }
            
        except Exception as e:
            logger.error(f"Erro no upload simulado: {str(e)}")
            raise Exception(f"Falha no upload simulado: {str(e)}")
    
    def delete_file(self, mega_file_id, account_id):
        """Simular eliminação de ficheiro do MEGA"""
        try:
            # Remover do armazenamento simulado
            if mega_file_id in self.mock_files:
                del self.mock_files[mega_file_id]
            
            logger.info(f"Ficheiro {mega_file_id} eliminado (simulado) da conta {account_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao eliminar ficheiro simulado: {str(e)}")
            raise Exception(f"Falha na eliminação simulada: {str(e)}")
    
    def update_account_space(self, account_id):
        """Simular atualização de informações de espaço"""
        try:
            account = MegaAccount.query.get(account_id)
            if not account:
                raise Exception("Conta não encontrada")
            
            # Simular valores de quota
            if account.total_space == 0:
                account.total_space = 50 * 1024 * 1024 * 1024  # 50GB
            
            # Simular variação no espaço usado
            variation = random.randint(-1024*1024, 1024*1024)  # ±1MB
            account.used_space = max(0, account.used_space + variation)
            account.last_updated = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Espaço simulado atualizado para conta {account.email}")
            
            return {
                'total_space': account.total_space,
                'used_space': account.used_space,
                'available_space': account.total_space - account.used_space
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar espaço simulado: {str(e)}")
            raise Exception(f"Falha na atualização simulada: {str(e)}")
    
    def test_account_connection(self, email, password):
        """Simular teste de conexão com conta MEGA"""
        try:
            # Simular tempo de conexão
            time.sleep(1)
            
            # Simular sucesso para qualquer email/password válidos
            if "@" in email and len(password) >= 6:
                return {
                    'success': True,
                    'total_space': 50 * 1024 * 1024 * 1024,  # 50GB
                    'used_space': random.randint(0, 10 * 1024 * 1024 * 1024)  # 0-10GB usado
                }
            else:
                return {
                    'success': False,
                    'error': 'Credenciais inválidas (simulação)'
                }
            
        except Exception as e:
            logger.error(f"Erro ao testar conta simulada: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_account_files(self, account_id):
        """Simular obtenção de lista de ficheiros"""
        try:
            # Filtrar ficheiros desta conta
            account_files = []
            for file_id, file_info in self.mock_files.items():
                if file_info['account_id'] == account_id:
                    account_files.append({
                        'id': file_id,
                        'name': file_info['filename'],
                        'size': file_info['size'],
                        'created': int(file_info['upload_date'].timestamp())
                    })
            
            return account_files
            
        except Exception as e:
            logger.error(f"Erro ao obter ficheiros simulados: {str(e)}")
            raise Exception(f"Falha ao obter ficheiros simulados: {str(e)}")
    
    def clear_client_cache(self, account_id=None):
        """Simular limpeza de cache"""
        logger.info("Cache simulado limpo")

# Instância global do serviço simulado
mega_service = MegaServiceMock()

