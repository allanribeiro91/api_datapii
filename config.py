import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração do banco de dados
DB_DIALECT = os.getenv("DB_DIALECT", "postgresql")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "omegao1tao")
DB_DATABASE = os.getenv("DB_DATABASE", "dbdatapii")
DB_SCHEMA = os.getenv("DB_SCHEMA", "sc_outputs")

DATABASE_URL = f"{DB_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"options": f"-c search_path={DB_SCHEMA}"})

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base declarativa
Base = declarative_base()
