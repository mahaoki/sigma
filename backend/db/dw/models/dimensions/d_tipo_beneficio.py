from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DTipoBeneficio(DwBase):
    __tablename__ = 'd_tipo_beneficio'

    id_tipo_beneficio = Column(Integer, primary_key=True, autoincrement=True)
    codigo_tipo_beneficio = Column(Integer, unique=True, nullable=False)
    nome_tipo_beneficio = Column(String(150), nullable=False)
    
    def __repr__(self):
        return f"<DTipoBeneficio(nome='{self.nome_tipo_beneficio}')>"
