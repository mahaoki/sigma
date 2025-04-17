from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from backend.database.dw.models.base import DwBase

class DCategoriaItemCatalogo(DwBase):
    __tablename__ = 'd_categoria_item_catalogo'

    id_categoria_item_catalogo = Column(Integer, primary_key=True, autoincrement=True)
    categoria_codigo = Column(Integer, unique=True, nullable=False)
    nome_categoria = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    status_ativo = Column(Boolean, nullable=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return (f"<DCategoriaItemCatalogo(nome_categoria='{self.nome_categoria}', "
                f"categoria_codigo={self.categoria_codigo})>")
