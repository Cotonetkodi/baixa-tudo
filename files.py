from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from src.models.file import File, db
from src.models.mega_account import MegaAccount
from src.services.mega_service_mock import mega_service

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload de ficheiros"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum ficheiro enviado'}), 400
        
        file = request.files['file']
        category = request.form.get('category')
        upload_id = request.form.get('upload_id')
        file_index = request.form.get('file_index', 0)
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum ficheiro selecionado'}), 400
        
        if not category:
            return jsonify({'error': 'Categoria não especificada'}), 400
        
        # Validar tamanho do ficheiro (5GB)
        max_size = 5 * 1024 * 1024 * 1024  # 5GB em bytes
        
        # Obter tamanho do ficheiro
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_size:
            return jsonify({'error': 'Ficheiro muito grande (máximo 5GB)'}), 413
        
        # Nome seguro do ficheiro
        original_filename = secure_filename(file.filename)
        
        try:
            # Upload para MEGA
            upload_result = mega_service.upload_file(
                file_data=file,
                filename=original_filename,
                category=category,
                file_size=file_size
            )
            
            # Criar registo na base de dados
            new_file = File(
                filename=original_filename,
                mega_filename=upload_result['mega_filename'],
                size=file_size,
                category=category,
                mega_account_id=upload_result['mega_account_id'],
                mega_file_id=upload_result['mega_file_id'],
                share_link=upload_result['share_link']
            )
            
            db.session.add(new_file)
            db.session.commit()
            
            current_app.logger.info(f"Ficheiro {original_filename} carregado com sucesso")
            
            return jsonify({
                'success': True,
                'file_id': new_file.id,
                'filename': original_filename,
                'share_link': new_file.share_link,
                'message': 'Ficheiro carregado com sucesso'
            })
            
        except Exception as mega_error:
            current_app.logger.error(f"Erro no upload para MEGA: {str(mega_error)}")
            return jsonify({'error': f'Erro no upload: {str(mega_error)}'}), 500
        
    except Exception as e:
        current_app.logger.error(f"Erro no upload: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@files_bp.route('/files', methods=['GET'])
def get_files():
    """Endpoint para obter lista de ficheiros"""
    try:
        files = File.query.order_by(File.upload_date.desc()).all()
        files_data = [file.to_dict() for file in files]
        return jsonify(files_data)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter ficheiros: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@files_bp.route('/files/search', methods=['GET'])
def search_files():
    """Endpoint para pesquisar ficheiros"""
    try:
        search_term = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        
        query = File.query
        
        # Filtrar por termo de pesquisa
        if search_term:
            query = query.filter(File.filename.contains(search_term))
        
        # Filtrar por categoria
        if category:
            query = query.filter(File.category == category)
        
        files = query.order_by(File.upload_date.desc()).all()
        files_data = [file.to_dict() for file in files]
        
        return jsonify(files_data)
        
    except Exception as e:
        current_app.logger.error(f"Erro na pesquisa: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@files_bp.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    """Endpoint para obter detalhes de um ficheiro específico"""
    try:
        file = File.query.get_or_404(file_id)
        return jsonify(file.to_dict())
    except Exception as e:
        current_app.logger.error(f"Erro ao obter ficheiro: {str(e)}")
        return jsonify({'error': 'Ficheiro não encontrado'}), 404

@files_bp.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Endpoint para eliminar um ficheiro"""
    try:
        file = File.query.get_or_404(file_id)
        
        try:
            # Eliminar do MEGA
            mega_service.delete_file(file.mega_file_id, file.mega_account_id)
            
            # Atualizar espaço usado da conta
            account = MegaAccount.query.get(file.mega_account_id)
            if account:
                account.used_space = max(0, account.used_space - file.size)
                account.last_updated = datetime.utcnow()
            
            # Eliminar da base de dados
            db.session.delete(file)
            db.session.commit()
            
            return jsonify({'message': 'Ficheiro eliminado com sucesso'})
            
        except Exception as mega_error:
            current_app.logger.error(f"Erro ao eliminar do MEGA: {str(mega_error)}")
            # Mesmo que falhe no MEGA, eliminar da base de dados
            db.session.delete(file)
            db.session.commit()
            return jsonify({'message': 'Ficheiro eliminado da base de dados (pode ainda existir no MEGA)'})
        
    except Exception as e:
        current_app.logger.error(f"Erro ao eliminar ficheiro: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@files_bp.route('/stats', methods=['GET'])
def get_stats():
    """Endpoint para obter estatísticas do sistema"""
    try:
        total_files = File.query.count()
        total_size = db.session.query(db.func.sum(File.size)).scalar() or 0
        
        # Estatísticas por categoria
        categories_stats = db.session.query(
            File.category,
            db.func.count(File.id).label('count'),
            db.func.sum(File.size).label('total_size')
        ).group_by(File.category).all()
        
        categories_data = []
        for category, count, size in categories_stats:
            categories_data.append({
                'category': category,
                'count': count,
                'total_size': size or 0
            })
        
        return jsonify({
            'total_files': total_files,
            'total_size': total_size,
            'categories': categories_data
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter estatísticas: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

