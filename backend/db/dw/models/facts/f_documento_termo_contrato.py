from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FDocumentoTermoContrato(DwBase):
    __tablename__ = 'f_documento_termo_contrato'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_termo_contrato = Column(Integer, ForeignKey('f_termo_contrato.id_termo_contrato'), nullable=False)
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_tipo_documento = Column(Integer, ForeignKey('d_tipo_documento.id_tipo_documento'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_documento = Column(Integer, nullable=True)
    sequencial_compra = Column(Integer, nullable=True)
    ano_compra = Column(Integer, nullable=True)
    titulo = Column(Text, nullable=True)
    uri = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    status_ativo = Column(Boolean, default=True)

    termo_contrato = relationship('FTermoContrato', foreign_keys=[id_termo_contrato], back_populates='documentos_termo')
    orgao = relationship('DOrgao', foreign_keys=[id_orgao], back_populates='documentos_termo')
    tipo_documento = relationship('DTipoDocumento', foreign_keys=[id_tipo_documento], back_populates='documentos_termo')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='documentos_termo_contrato_publicacao')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='documentos_termo_contrato_publicacao')

    __table_args__ = (
        Index('idx_f_documento_termo_data_etl', 'data_etl'),
        Index('idx_f_documento_termo_id_termo', 'id_termo_contrato'),
        Index('idx_f_documento_termo_id_orgao', 'id_orgao'),
        Index('idx_f_documento_termo_id_tipo_documento', 'id_tipo_documento'),
        Index('idx_f_documento_termo_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_documento_termo_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_documento_termo_sequencial_documento', 'sequencial_documento'),
        Index('idx_f_documento_termo_status_ativo', 'status_ativo'),
    )

    __table_args__ = (
        Index('idx_doc_termo_publicacao', 'id_tempo_publicacao', 'id_orgao'),
    )