"""
Script para inicializar o administrador padrão
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def init_default_admin():
    """Criar administrador padrão se não existir"""
    from src.main import app
    from src.models.admin import Admin, db
    
    with app.app_context():
        # Verificar se já existe um administrador
        existing_admin = Admin.query.first()
        
        if not existing_admin:
            # Criar administrador padrão
            admin = Admin(username='admin')
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("Administrador padrão criado:")
            print("Utilizador: admin")
            print("Palavra-passe: admin123")
            print("IMPORTANTE: Altere estas credenciais após o primeiro login!")
        else:
            print("Administrador já existe na base de dados.")

if __name__ == '__main__':
    init_default_admin()

