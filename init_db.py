from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base  
from config import DATABASE_URL 

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Criar a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_schema_and_table():
    """Cria o schema e a tabela se não existirem."""
    with engine.connect() as connection:
        # Criar schema se não existir
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS sc_outputs;"))
        connection.commit()  # Confirma a criação do schema

        # Criar tabelas no banco de dados
        Base.metadata.create_all(engine)

    print("✅ Schema e tabela verificados/criados com sucesso!")

if __name__ == "__main__":
    create_schema_and_table()
