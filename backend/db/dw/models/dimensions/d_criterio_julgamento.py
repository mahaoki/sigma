from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DCriterioJulgamento(DwBase):
    __tablename__ = 'd_criterio_julgamento'

    id_criterio_julgamento = Column(Integer, primary_key=True, autoincrement=True)
    codigo_criterio_julgamento = Column(Integer, unique=True, nullable=False)
    nome_criterio_julgamento = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<DCriterioJulgamento(nome='{self.nome_criterio_julgamento}')>"
