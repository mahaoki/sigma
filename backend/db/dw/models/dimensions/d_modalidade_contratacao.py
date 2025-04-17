from sqlalchemy import Column, Integer, String
from backend.database.dw.models.base import DwBase
from sqlalchemy.orm import relationship

class DModalidadeContratacao(DwBase):
    __tablename__ = 'd_modalidade_contratacao'
    id_modalidade = Column(Integer, primary_key=True, autoincrement=True)
    modalidade_nome = Column(String(150), nullable=False)
    modalidade_codigo = Column(Integer, unique=True, nullable=True)

    contratacoes = relationship('FContratacao', foreign_keys='FContratacao.id_modalidade', back_populates='modalidade')
    atas = relationship('FAtaRegistroPreco',foreign_keys='FAtaRegistroPreco.id_modalidade', back_populates='modalidade')

    def __repr__(self):
        return f"<DModalidadeContratacao(modalidade='{self.modalidade_nome}')>"
