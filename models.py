from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import declarative_base
from config import Base

class GeneralNumbers(Base):
    __tablename__ = "tb_general_numbers"
    __table_args__ = {"schema": "sc_outputs"}  # Definir o schema corretamente

    id = Column(Integer, primary_key=True, index=True, name="ID")  # Mapeia "ID" do banco
    data_reference = Column(Date, nullable=False, name="DATA_REFERENCE")
    name = Column(String(64), nullable=False, name="NAME")
    value = Column(Float, nullable=False, name="VALUE")
    descricao = Column(Text, nullable=True, name="DESCRICAO")  # Pode ser NULL
