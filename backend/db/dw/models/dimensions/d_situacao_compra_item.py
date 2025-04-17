from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase

class DSituacaoCompraItem(DwBase):
    __tablename__ = 'd_situacao_compra_item'

    id_situacao_compra_item = Column(Integer, primary_key=True, autoincrement=True)
    codigo_situacao_compra_item = Column(Integer, unique=True, nullable=False)
    nome_situacao_compra_item = Column(String(150), nullable=False)

    def __repr__(self):
        return f"<DSituacaoCompraItem(nome='{self.nome_situacao_compra_item}')>"
