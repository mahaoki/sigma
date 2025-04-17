from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DCategoriaProcesso(DwBase):
    __tablename__ = 'd_categoria_processo'

    id_categoria = Column(Integer, primary_key=True)
    categoria_codigo = Column(Integer, unique=True, nullable=False) # novo campo
    nome_categoria = Column(String(150), nullable=False)

    def __repr__(self):
        return f"<DCategoriaProcesso(nome_categoria='{self.nome_categoria}')>"
