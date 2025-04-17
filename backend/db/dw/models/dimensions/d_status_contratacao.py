from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DStatusContratacao(DwBase):
    __tablename__ = 'd_status_contratacao'

    id_status_contratacao = Column(Integer, primary_key=True, autoincrement=True)
    situacao_compra_id = Column(Integer, unique=True, nullable=True)
    nome_situacao = Column(String(100), nullable=True)

    # Relacionamento explícito com FContratacao
    contratacoes = relationship('FContratacao', back_populates='status_contratacao')

    def __repr__(self):
        return f"<DStatusContratacao(situacao_compra_id='{self.situacao_compra_id}', nome_situacao='{self.nome_situacao}')>"