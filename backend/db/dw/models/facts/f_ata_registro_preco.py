from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FAtaRegistroPreco(DwBase):
    __tablename__ = 'f_ata_registro_preco'

    id_ata = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_contratacao = Column(Integer, ForeignKey('f_contratacao.id_contratacao'), nullable=False)

    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_orgao_sub_rogado = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=True)

    id_unidade_administrativa = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'))
    id_unidade_sub_rogada = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'), nullable=True)

    id_modalidade = Column(Integer, ForeignKey('d_modalidade_contratacao.id_modalidade'))

    id_tempo_inclusao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_assinatura = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_inicio = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_fim = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_cancelamento = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))

    id_hora_inclusao = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_assinatura = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_vigencia_inicio = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_vigencia_fim = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_cancelamento = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    ano_ata = Column(Integer)
    sequencial_ata = Column(Integer)
    numero_ata_registro_preco = Column(String(50))
    objeto_compra = Column(Text)
    cancelado = Column(Boolean)
    numero_controle_pncp = Column(String(100))
    informacao_complementar_compra = Column(Text)
    data_atualizacao = Column(TIMESTAMP)
    data_atualizacao_global = Column(TIMESTAMP)

    contratacao = relationship('FContratacao', back_populates='atas')
    documentos_ata = relationship('FDocumentoAta', back_populates='atas')

    orgao = relationship('DOrgao', foreign_keys=[id_orgao], back_populates='atas')
    orgao_sub_rogado = relationship('DOrgao', foreign_keys=[id_orgao_sub_rogado], back_populates='atas_subrogadas')

    unidade_administrativa = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_administrativa], back_populates='atas')
    unidade_sub_rogada = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_sub_rogada], back_populates='atas_subrogadas')

    modalidade = relationship('DModalidadeContratacao', back_populates='atas')

    tempo_inclusao = relationship('DTempo', foreign_keys=[id_tempo_inclusao], back_populates='atas_inclusao')
    tempo_assinatura = relationship('DTempo', foreign_keys=[id_tempo_assinatura], back_populates='atas_assinatura')
    tempo_vigencia_inicio = relationship('DTempo', foreign_keys=[id_tempo_vigencia_inicio], back_populates='atas_vigencia_inicio')
    tempo_vigencia_fim = relationship('DTempo', foreign_keys=[id_tempo_vigencia_fim], back_populates='atas_vigencia_fim')
    tempo_cancelamento = relationship('DTempo', foreign_keys=[id_tempo_cancelamento], back_populates='atas_cancelamento')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='atas_publicacao')

    hora_inclusao = relationship('DHora', foreign_keys=[id_hora_inclusao], back_populates='atas_inclusao')
    hora_assinatura = relationship('DHora', foreign_keys=[id_hora_assinatura], back_populates='atas_assinatura')
    hora_cancelamento = relationship('DHora', foreign_keys=[id_hora_cancelamento], back_populates='atas_cancelamento')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='atas_publicacao')

    __table_args__ = (
        Index('idx_f_ata_data_etl', 'data_etl'),
        Index('idx_f_ata_id_contratacao', 'id_contratacao'),
        Index('idx_f_ata_id_orgao', 'id_orgao'),
        Index('idx_f_ata_id_unidade_administrativa', 'id_unidade_administrativa'),
        Index('idx_f_ata_id_modalidade', 'id_modalidade'),
        Index('idx_f_ata_id_tempo_inclusao', 'id_tempo_inclusao'),
        Index('idx_f_ata_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_ata_id_tempo_assinatura', 'id_tempo_assinatura'),
        Index('idx_f_ata_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_ata_numero_controle_pncp', 'numero_controle_pncp'),
    )

    def __repr__(self):
        return f"<FAtaRegistroPreco(id_staging='{self.id_staging}', numero_controle_pncp={self.numero_controle_pncp})>"

