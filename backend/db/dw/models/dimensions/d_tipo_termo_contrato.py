from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DTipoTermoContrato(DwBase):
    __tablename__ = 'd_tipo_termo_contrato'

    id_tipo_termo_contrato = Column(Integer, primary_key=True, autoincrement=True)
    codigo_tipo_termo_contrato = Column(Integer, unique=True, nullable=False)  # novo campo
    nome_tipo_termo_contrato = Column(String(150), nullable=False)

    def __repr__(self):
        return f"<DTipoTermoContrato(nome_tipo='{self.nome_tipo_termo_contrato}')>"
