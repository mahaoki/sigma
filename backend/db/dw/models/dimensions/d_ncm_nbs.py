from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DNcmNbs(DwBase):
    __tablename__ = 'd_ncm_nbs'

    id_ncm_nbs = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)

    itens_nfe = relationship('FNotaFiscalItem', back_populates='ncm_nbs')

    __table_args__ = (
        Index('idx_dncm_nbs_codigo', 'codigo'),
    )

    def __repr__(self):
        return f"<DNcmNbs(codigo='{self.codigo}', descricao='{self.descricao}')>"
