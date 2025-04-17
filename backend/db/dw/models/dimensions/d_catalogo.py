from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from backend.database.dw.models.base import DwBase

class DCatalogo(DwBase):
    __tablename__ = 'd_catalogo'

    id_catalogo = Column(Integer, primary_key=True, autoincrement=True)
    catalogo_codigo = Column(Integer, unique=True, nullable=False)
    nome_catalogo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)
    status_ativo = Column(Boolean, nullable=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"<DCatalogo(nome_catalogo='{self.nome_catalogo}', codigo={self.catalogo_codigo})>"
