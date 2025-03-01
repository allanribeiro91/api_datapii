from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import func
from config import SessionLocal, engine
import models
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, verify_jwt_token

#FASTAPI
app = FastAPI()

#SWAGGER
# Customização do Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DataPii",
        version="1.0.0",
        description="API para gerenciar rotas de dados da Embrapii.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

#BANCO DE DADOS
# Criar tabelas no banco de dados (caso ainda não existam)
models.Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#ROTAS

# Rota para autenticação e geração do token JWT
@app.post("/token", tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para buscar todos os registros da tabela tb_general_numbers
@app.get("/general-numbers/latest", tags=["Site Embrapii"])
def get_general_numbers(db: Session = Depends(get_db), user: dict = Depends(verify_jwt_token)):
    # Encontrar a maior data disponível
    max_date = db.query(func.max(models.GeneralNumbers.data_reference)).scalar()

    if max_date is None:
        return {"message": "Nenhum dado encontrado"}

    # Buscar os registros com a maior data encontrada
    records = db.query(models.GeneralNumbers).filter(models.GeneralNumbers.data_reference == max_date).all()
    
    return records

@app.get("/general-numbers/all", tags=["Site Embrapii"])
def get_general_numbers(db: Session = Depends(get_db), authorized: bool = Depends(verify_jwt_token)):

    # Buscar os registros com a maior data encontrada
    records = db.query(models.GeneralNumbers).all()
    
    return records

# Modelo para validação dos dados recebidos via API
class GeneralNumbersCreate(BaseModel):
    data_reference: str
    name: str
    value: float
    descricao: str | None = None


# Rota para inserir um novo registro
@app.post("/general-numbers", status_code=201, tags=["Site Embrapii"])
def create_general_number(
    general_number: GeneralNumbersCreate,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_jwt_token)
):
    new_record = models.GeneralNumbers(
        data_reference=general_number.data_reference,
        name=general_number.name,
        value=general_number.value,
        descricao=general_number.descricao
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "Registro criado com sucesso!", "data": new_record}
