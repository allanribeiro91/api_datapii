import os
import jwt
import datetime
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave secreta e algoritmo
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token válido por 60 minutos

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definição do esquema OAuth2 para proteção de rotas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulação de usuário
fake_users_db = {
    "admin": {
        "username": USERNAME,
        "password": pwd_context.hash(PASSWORD)
    }
}

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para autenticar usuário
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

# Função para criar um JWT Token
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para verificar JWT Token
def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
