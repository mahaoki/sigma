from sqlalchemy import Column, Integer, String, UniqueConstraint
from backend.database.dw.models.base import DwBase

class DTipoInstrumentoConvocatorio(DwBase):
    __tablename__ = 'd_tipo_instrumento_convocatorio'

    id_tipo_instrumento_convocatorio = Column(Integer, primary_key=True, autoincrement=True)
    nome_instrumento_convocatorio = Column(String(150), nullable=False)
    codigo_instrumento_convocatorio = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('codigo_instrumento_convocatorio', name='uq_codigo_instrumento_convocatorio'),
    )

    def __repr__(self):
        return (
            f"<DTipoInstrumentoConvocatorio("
            f"nome='{self.nome_instrumento_convocatorio}', "
            f"codigo='{self.codigo_instrumento_convocatorio}')>"
        )
