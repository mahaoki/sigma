from sqlalchemy import Column, Integer, String, Index
from backend.database.dw.models.base import DwBase

class DEventoNotaFiscal(DwBase):
    __tablename__ = 'd_evento_nota_fiscal'

    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    tipo_evento = Column(String(100), unique=True, nullable=False, index=True)
    evento = Column(String(255), nullable=False)
    motivo_evento = Column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_evento_nf_tipo_evento', 'tipo_evento'),
    )

    def __repr__(self):
        return (f"<DEventoNotaFiscal(tipo_evento='{self.tipo_evento}', "
                f"evento='{self.evento}', motivo_evento='{self.motivo_evento}')>")
