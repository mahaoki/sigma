from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FNotaFiscalEvento(DwBase):
    __tablename__ = 'f_nota_fiscal_evento'

    id_nota_fiscal_evento = Column(Integer, primary_key=True, autoincrement=True)
    id_nota_fiscal = Column(Integer, ForeignKey('d_nota_fiscal.id_nota_fiscal'), nullable=False)

    tipo_evento = Column(String(100), nullable=False)
    evento = Column(String(255), nullable=False)
    motivo_evento = Column(String(500), nullable=True)
    data_evento = Column(TIMESTAMP, nullable=False)

    data_inclusao = Column(TIMESTAMP, nullable=True)

    # Relacionamentos
    nota_fiscal = relationship('DNotaFiscal', back_populates='eventos')

    __table_args__ = (
        Index('idx_f_nf_evento_id_nota_fiscal', 'id_nota_fiscal'),
        Index('idx_f_nf_evento_tipo_evento', 'tipo_evento'),
    )

    def __repr__(self):
        return (f"<FNotaFiscalEvento(tipo_evento='{self.tipo_evento}', "
                f"data_evento='{self.data_evento}')>")
