from sqlalchemy import Column, Integer, Text, Boolean, String, ForeignKey, Index, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FDocumentoContratacao(DwBase):
    __tablename__ = 'f_documento_contratacao'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_contratacao = Column(Integer, ForeignKey('f_contratacao.id_contratacao'), nullable=False)
    id_orgao = Column(Integer, ForeignKey("d_orgao.id_orgao"), nullable=False)
    id_tipo_documento = Column(Integer, ForeignKey('d_tipo_documento.id_tipo_documento'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_documento = Column(Integer)
    sequencial_compra = Column(Integer)
    ano_compra = Column(Integer)
    titulo = Column(Text)
    status_ativo = Column(Boolean)
    uri = Column(Text)
    url = Column(Text)
    
    contratacao = relationship('FContratacao', back_populates='documentos_contratacao')
    orgao = relationship('DOrgao', back_populates='documentos_contratacao')
    tipo_documento = relationship('DTipoDocumento', back_populates='documentos_contratacao')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='documentos_contratacao_publicacao')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='documentos_contratacao_publicacao')


    __table_args__ = (
        Index('idx_f_documento_contratacao_data_etl', 'data_etl'),
        Index('idx_f_documento_contratacao_id_contratacao', 'id_contratacao'),
        Index('idx_f_documento_contratacao_id_orgao', 'id_orgao'),
        Index('idx_f_documento_contratacao_id_tipo_documento', 'id_tipo_documento'),
        Index('idx_f_documento_contratacao_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_documento_contratacao_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_documento_contratacao_sequencial_documento', 'sequencial_documento'),
        Index('idx_f_documento_contratacao_status_ativo', 'status_ativo'),
    )

    def __repr__(self):
        return f"<FDocumentoContratacao(id_documento={self.id_documento}, titulo='{self.titulo[:30]}...')>"