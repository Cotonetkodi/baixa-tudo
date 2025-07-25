import os
from cryptography.fernet import Fernet
import base64

def get_encryption_key():
    """Obtém a chave de encriptação das variáveis de ambiente"""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Gerar uma chave se não existir (apenas para desenvolvimento)
        key = Fernet.generate_key().decode()
        print(f"Generated encryption key: {key}")
        print("Please set this as ENCRYPTION_KEY environment variable")
    
    # Garantir que a chave tem o formato correto
    if isinstance(key, str):
        key = key.encode()
    
    return base64.urlsafe_b64encode(key[:32].ljust(32, b'0'))

def encrypt_password(password):
    """Encripta uma palavra-passe"""
    if not password:
        return None
    
    key = get_encryption_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password):
    """Desencripta uma palavra-passe"""
    if not encrypted_password:
        return None
    
    key = get_encryption_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

