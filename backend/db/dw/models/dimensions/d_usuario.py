from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DUsuario(DwBase):
    __tablename__ = 'd_usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<DUsuario(nome_usuario='{self.nome_usuario}')>"
