from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase
class DPoder(DwBase):
    __tablename__ = 'd_poder'

    id_poder = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(2), unique=True, nullable=False)  # "N", "L", "J"
    descricao = Column(String(50), nullable=False)  # Executivo, Legislativo, Judiciário

    def __repr__(self):
        return f"<DPoder(codigo='{self.codigo}', descricao='{self.descricao}')>"
