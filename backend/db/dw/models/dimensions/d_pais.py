from sqlalchemy import Column, String, CHAR
from backend.database.dw.models.base import DwBase

class DPais(DwBase):
    __tablename__ = 'd_pais'

    codigo_pais = Column(CHAR(3), primary_key=True)
    nome_pais = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<DPais(codigo_pais='{self.codigo_pais}', nome_pais='{self.nome_pais}')>"
