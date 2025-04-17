from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DEsfera(DwBase):
    __tablename__ = 'd_esfera'

    id_esfera = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(2), unique=True, nullable=False)  # Ex: "M", "E", "F"
    descricao = Column(String(50), nullable=False)  # Municipal, Estadual, Federal

    def __repr__(self):
        return f"<DEsfera(codigo='{self.codigo}', descricao='{self.descricao}')>"
