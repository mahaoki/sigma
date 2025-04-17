from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DSituacaoResultado(DwBase):
    __tablename__ = 'd_situacao_resultado'

    id_situacao = Column(Integer, primary_key=True, autoincrement=True)
    situacao_codigo = Column(Integer, unique=True, nullable=False)
    nome_situacao = Column(String(150), nullable=False)

    resultados = relationship("FResultadoItem", backref="situacao_resultado")

    def __repr__(self):
        return f"<DSituacaoResultado(nome='{self.nome_situacao}')>"
