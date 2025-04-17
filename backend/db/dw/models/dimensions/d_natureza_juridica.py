from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DNaturezaJuridica(DwBase):
    __tablename__ = 'd_natureza_juridica'

    id_natureza_juridica = Column(Integer, primary_key=True, autoincrement=True)
    codigo_natureza_juridica = Column(Integer, unique=True, nullable=False)
    nome_natureza_juridica = Column(String(255), nullable=False)

    fornecedores = relationship("DFornecedor", back_populates="natureza_juridica")

    def __repr__(self):
        return f"<DNaturezaJuridica(nome='{self.nome_natureza_juridica}')>"
