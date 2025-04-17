from sqlalchemy import Column, Integer, String, Boolean
from backend.database.dw.models.base import DwBase

class DTipoContrato(DwBase):
    __tablename__ = 'd_tipo_contrato'

    id_tipo_contrato = Column(Integer, primary_key=True)
    codigo_tipo_contrato = Column(Integer, unique=True, nullable=False) # novo campo
    nome_tipo_contrato = Column(String(150), nullable=False)
    status_ativo = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<DTipoContrato(nome='{self.nome_tipo_contrato}', ativo={self.status_ativo})>"
