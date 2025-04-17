from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from backend.database.dw.models.base import DwBase

class DAmparoLegal(DwBase):
    __tablename__ = 'd_amparo_legal'

    id_amparo_legal = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    codigo = Column(Integer, nullable=False, unique=True)
    descricao = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=True)  # Novo campo: tipo do amparo legal

    __table_args__ = (
        UniqueConstraint('codigo', name='uq_d_amparo_legal_codigo'),
    )

    def __repr__(self):
        return f"<DAmparoLegal(nome='{self.nome}', codigo='{self.codigo}', tipo='{self.tipo}')>"
