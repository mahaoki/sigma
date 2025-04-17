from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DMotivoCancelamento(DwBase):
    __tablename__ = 'd_motivo_cancelamento'

    id_motivo_cancelamento = Column(Integer, primary_key=True, autoincrement=True)
    descricao_motivo = Column(String(255), unique=True, nullable=False)

    resultados = relationship("FResultadoItem", backref="motivo_cancelamento")

    def __repr__(self):
        return f"<DMotivoCancelamento(motivo='{self.descricao_motivo}')>"
