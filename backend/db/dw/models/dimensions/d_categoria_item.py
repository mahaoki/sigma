from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DCategoriaItem(DwBase):
    __tablename__ = 'd_categoria_item'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    categoria_codigo = Column(Integer, unique=True, nullable=False) # Novo campo
    nome_categoria = Column(String(150), nullable=False)

    def __repr__(self):
        return f"<DCategoriaItem(nome_categoria='{self.nome_categoria}')>"
