from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, CHAR, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FTermoContrato(DwBase):
    __tablename__ = 'f_termo_contrato'

    id_termo_contrato = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_contrato = Column(Integer, ForeignKey('f_contrato.id_contrato'), nullable=False)
    
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_orgao_sub_rogado = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=True)
    id_unidade_administrativa = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'))
    id_unidade_sub_rogada = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'), nullable=True)
    
    id_fornecedor = Column(Integer, ForeignKey('d_fornecedor.id_fornecedor'))
    id_tipo_termo_contrato = Column(Integer, ForeignKey('d_tipo_termo_contrato.id_tipo_termo_contrato'))

    id_tempo_assinatura = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_inclusao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_inicio = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_fim = Column(Integer, ForeignKey('d_tempo.id_tempo'))

    id_hora_assinatura = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_inclusao = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_termo_contrato = Column(Integer)
    numero_termo_contrato = Column(String(50))
    processo = Column(String(50))
    objeto_termo_contrato = Column(Text)
    tipo_pessoa = Column(CHAR(2))
    valor_global = Column(Numeric(15,2))
    valor_parcela = Column(Numeric(15,2))
    numero_parcelas = Column(Integer)
    fundamento_legal = Column(Text)
    prazo_aditado_dias = Column(Integer)
    qualificacao_reajuste = Column(Boolean)
    qualificacao_vigencia = Column(Boolean)
    qualificacao_fornecedor = Column(Boolean)
    qualificacao_acrescimo_supressao = Column(Boolean)
    informacao_complementar = Column(Text)
    informativo_observacao = Column(Text)
    data_atualizacao = Column(TIMESTAMP)
    excluido = Column(Boolean, default=False)
    valor_acrescido = Column(Numeric(15, 2))
    numero_contrato_empenho = Column(String(50))
    tipo_pessoa_sub_contratada = Column(String(10))
    ni_fornecedor_sub_contratado = Column(String(20))
    nome_fornecedor_sub_contratado = Column(String(150))

    documentos = relationship('FDocumentoTermoContrato', backref='termos_contrato')
    
    contrato = relationship('FContrato', foreign_keys=[id_contrato], back_populates='termos_contrato')
    orgao = relationship('DOrgao', foreign_keys=[id_orgao], back_populates='termos_contrato')
    orgao_sub_rogado = relationship('DOrgao', foreign_keys=[id_orgao_sub_rogado], back_populates='termos_contrato_subrogados')

    unidade_administrativa = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_administrativa], back_populates='termos_contrato')
    unidade_sub_rogada = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_sub_rogada], back_populates='termos_contrato_subrogadas')

    fornecedor = relationship('DFornecedor')
    tipo_termo_contrato = relationship('DTipoTermoContrato')

    tempo_assinatura = relationship('DTempo', foreign_keys=[id_tempo_assinatura], back_populates='termos_contrato_assinatura')
    tempo_inclusao = relationship('DTempo', foreign_keys=[id_tempo_inclusao], back_populates='termos_contrato_inclusao')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='termos_contrato_publicacao')
    tempo_vigencia_inicio = relationship('DTempo', foreign_keys=[id_tempo_vigencia_inicio], back_populates='termos_contrato_vigencia_inicio')
    tempo_vigencia_fim = relationship('DTempo', foreign_keys=[id_tempo_vigencia_fim], back_populates='termos_contrato_vigencia_fim')

    hora_assinatura = relationship('DHora', foreign_keys=[id_hora_assinatura], back_populates='termos_contrato_assinatura')
    hora_inclusao = relationship('DHora', foreign_keys=[id_hora_inclusao], back_populates='termos_contrato_inclusao')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='termos_contrato_publicacao')

    documentos_termo = relationship('FDocumentoTermoContrato', back_populates='termo_contrato', cascade='all, delete-orphan', lazy='selectin')

    __table_args__ = (
        Index('idx_f_termo_contrato_data_etl', 'data_etl'),
        Index('idx_f_termo_contrato_id_contrato', 'id_contrato'),
        Index('idx_f_termo_contrato_id_orgao', 'id_orgao'),
        Index('idx_f_termo_contrato_id_orgao_sub_rogado', 'id_orgao_sub_rogado'),
        Index('idx_f_termo_contrato_id_unidade_administrativa', 'id_unidade_administrativa'),
        Index('idx_f_termo_contrato_id_unidade_sub_rogada', 'id_unidade_sub_rogada'),
        Index('idx_f_termo_contrato_id_fornecedor', 'id_fornecedor'),
        Index('idx_f_termo_contrato_id_tipo_termo_contrato', 'id_tipo_termo_contrato'),
        Index('idx_f_termo_contrato_id_tempo_inclusao', 'id_tempo_inclusao'),
        Index('idx_f_termo_contrato_id_tempo_assinatura', 'id_tempo_assinatura'),
        Index('idx_f_termo_contrato_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_termo_contrato_id_tempo_vigencia_inicio', 'id_tempo_vigencia_inicio'),
        Index('idx_f_termo_contrato_id_tempo_vigencia_fim', 'id_tempo_vigencia_fim'),
        Index('idx_f_termo_contrato_id_hora_inclusao', 'id_hora_inclusao'),
        Index('idx_f_termo_contrato_id_hora_assinatura', 'id_hora_assinatura'),
        Index('idx_f_termo_contrato_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_termo_contrato_excluido', 'excluido'),
        Index('idx_f_termo_contrato_sequencial', 'sequencial_termo_contrato'),
    )

    def __repr__(self):
        return (
            f"<FTermoContrato(id_staging={self.id_staging}, "
            f"numero_termo='{self.numero_termo_contrato}', "
            f"valor_global={self.valor_global})>"
        )