from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DModoDisputa(DwBase):
    __tablename__ = 'd_modo_disputa'

    id_modo_disputa = Column(Integer, primary_key=True, autoincrement=True)
    modo_disputa_codigo = Column(Integer, nullable=False, unique=True) 
    modo_disputa_nome = Column(String(150), nullable=False)

    def __repr__(self):
        return f"<DModoDisputa(modo='{self.modo_disputa_nome}')>"
