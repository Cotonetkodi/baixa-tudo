import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from src.models.user import db
from src.models.file import File
from src.models.mega_account import MegaAccount
from src.models.admin import Admin
from src.routes.user import user_bp
from src.routes.files import files_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB

# Configurar CORS
CORS(app)

# Configurar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializar base de dados
db.init_app(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(files_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Criar tabelas e admin padrão
with app.app_context():
    db.create_all()
    
    # Criar administrador padrão se não existir
    if not Admin.query.first():
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Administrador padrão criado: admin/admin123")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
