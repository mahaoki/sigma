from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FDocumentoAta(DwBase):
    __tablename__ = 'f_documento_ata'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_ata = Column(Integer, ForeignKey('f_ata_registro_preco.id_ata'), nullable=False)
    id_tipo_documento = Column(Integer, ForeignKey('d_tipo_documento.id_tipo_documento'))

    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_documento = Column(Integer)
    titulo = Column(Text)
    url = Column(Text)
    status_ativo = Column(Boolean)

    tipo_documento = relationship('DTipoDocumento')
    atas = relationship('FAtaRegistroPreco', foreign_keys=[id_ata], back_populates='documentos_ata')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='documentos_ata_publicacao')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='documentos_ata_publicacao')

    __table_args__ = (
        Index('idx_f_documento_ata_data_etl', 'data_etl'),
        Index('idx_f_documento_ata_id_ata', 'id_ata'),
        Index('idx_f_documento_ata_id_tipo_documento', 'id_tipo_documento'),
        Index('idx_f_documento_ata_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_documento_ata_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_documento_ata_sequencial_documento', 'sequencial_documento'),
        Index('idx_f_documento_ata_status_ativo', 'status_ativo'),
    )

    def __repr__(self):
        return f"<FDocumentoAta(id_staging={self.id_staging}, id_ata={self.id_ata}, titulo='{self.titulo[:30]}...')>"

