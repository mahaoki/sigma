from sqlalchemy import Column, CHAR, String
from backend.database.dw.models.base import DwBase
class DMoeda(DwBase):
    __tablename__ = 'd_moeda'

    codigo_moeda = Column(CHAR(3), primary_key=True)  # ex.: "USD"
    nome_moeda = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<DMoeda(moeda='{self.codigo_moeda}', nome='{self.nome_moeda}')>"
