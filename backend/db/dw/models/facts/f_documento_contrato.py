from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FDocumentoContrato(DwBase):
    __tablename__ = 'f_documento_contrato'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_contrato = Column(Integer, ForeignKey('f_contrato.id_contrato'), nullable=False)
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_tipo_documento = Column(Integer, ForeignKey('d_tipo_documento.id_tipo_documento'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_documento = Column(Integer)
    sequencial_compra = Column(Integer)  # <- novo
    ano_compra = Column(Integer)         # <- novo
    status_ativo = Column(Boolean, default=True)  # <- novo (se quiser controlar isso)

    titulo = Column(Text)
    uri = Column(Text)
    url = Column(Text)

    
    orgao = relationship('DOrgao')
    tipo_documento = relationship('DTipoDocumento')
    contrato = relationship('FContrato', foreign_keys=[id_contrato], back_populates='documentos_contrato')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='documentos_contrato_publicacao')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='documentos_contrato_publicacao')

    __table_args__ = (
        Index('idx_f_documento_contrato_data_etl', 'data_etl'),
        Index('idx_f_documento_contrato_id_contrato', 'id_contrato'),
        Index('idx_f_documento_contrato_id_orgao', 'id_orgao'),
        Index('idx_f_documento_contrato_id_tipo_documento', 'id_tipo_documento'),
        Index('idx_f_documento_contrato_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_documento_contrato_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_documento_contrato_sequencial_documento', 'sequencial_documento'),
        Index('idx_f_documento_contrato_status_ativo', 'status_ativo'),
    )

    def __repr__(self):
        return (
            f"<FDocumentoContrato(id_staging={self.id_staging}, "
            f"titulo='{(self.titulo or '')[:40]}...')>"
        )
