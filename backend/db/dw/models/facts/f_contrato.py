from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FContrato(DwBase):
    __tablename__ = 'f_contrato'

    id_contrato = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=False, index=True)

    id_contratacao = Column(Integer, ForeignKey('f_contratacao.id_contratacao'), nullable=False)
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_orgao_sub_rogado = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=True)
    id_unidade_administrativa = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'))
    id_unidade_sub_rogada = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'), nullable=True)
    id_fornecedor = Column(Integer, ForeignKey('d_fornecedor.id_fornecedor'))
    id_tipo_contrato = Column(Integer, ForeignKey('d_tipo_contrato.id_tipo_contrato'))
    id_categoria_processo = Column(Integer, ForeignKey('d_categoria_processo.id_categoria'))
    id_usuario = Column(Integer, ForeignKey('d_usuario.id_usuario'))

    id_tempo_assinatura = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_inicio = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_vigencia_fim = Column(Integer, ForeignKey('d_tempo.id_tempo'))

    id_hora_assinatura = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))

    sequencial_contrato = Column(Integer)
    processo = Column(String(50), index=True)
    objeto_contrato = Column(Text)
    receita = Column(Boolean)

    valor_global = Column(Numeric(15, 2))
    valor_inicial = Column(Numeric(15, 2))
    valor_parcela = Column(Numeric(15, 2))
    numero_parcelas = Column(Integer)
    numero_retificacao = Column(Integer)

    numero_contrato_empenho = Column(String(50), index=True)
    informacao_complementar = Column(Text)
    numero_controle_pncp = Column(String(100), unique=True, index=True)
    numero_controle_pncp_compra = Column(String(100), index=True)
    data_atualizacao = Column(TIMESTAMP)
    data_atualizacao_global = Column(TIMESTAMP)
    url_cipi = Column(Text)
    identificador_cipi = Column(Text)

    ano_contrato = Column(Integer, index=True)
    valor_acumulado = Column(Numeric(15, 2))

    tipo_pessoa_subcontratada = Column(String(2))
    ni_fornecedor_subcontratado = Column(String(20))
    nome_fornecedor_subcontratado = Column(Text)

    contratacao = relationship('FContratacao', back_populates='contratos')

    documentos_contrato = relationship('FDocumentoContrato', back_populates='contrato')
    termos_contrato = relationship('FTermoContrato', back_populates='contrato')
    instrumentos_cobranca = relationship('FInstrumentoCobranca', back_populates='contrato')
    
    orgao = relationship('DOrgao', foreign_keys=[id_orgao], back_populates='contratos')
    orgao_sub_rogado = relationship('DOrgao', foreign_keys=[id_orgao_sub_rogado], back_populates='contratos_subrogados')

    unidade_administrativa = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_administrativa], back_populates='contratos')
    unidade_sub_rogada = relationship('DUnidadeAdministrativa', foreign_keys=[id_unidade_sub_rogada], back_populates='contratos_subrogadas')

    fornecedor = relationship('DFornecedor')
    tipo_contrato = relationship('DTipoContrato')
    categoria_processo = relationship('DCategoriaProcesso')
    usuario = relationship('DUsuario')

    tempo_assinatura = relationship('DTempo', foreign_keys=[id_tempo_assinatura], back_populates='contratos_assinatura')
    tempo_publicacao = relationship('DTempo', foreign_keys=[id_tempo_publicacao], back_populates='contratos_publicacao')
    tempo_vigencia_inicio = relationship('DTempo', foreign_keys=[id_tempo_vigencia_inicio], back_populates='contratos_vigencia_inicio')
    tempo_vigencia_fim = relationship('DTempo', foreign_keys=[id_tempo_vigencia_fim], back_populates='contratos_vigencia_fim')

    hora_assinatura = relationship('DHora', foreign_keys=[id_hora_assinatura], back_populates='contratos_assinatura')
    hora_publicacao = relationship('DHora', foreign_keys=[id_hora_publicacao], back_populates='contratos_publicacao')

    __table_args__ = (
        Index('idx_f_contrato_id_contratacao', 'id_contratacao'),
        Index('idx_f_contrato_id_orgao', 'id_orgao'),
        Index('idx_f_contrato_id_orgao_sub_rogado', 'id_orgao_sub_rogado'),
        Index('idx_f_contrato_id_unidade_administrativa', 'id_unidade_administrativa'),
        Index('idx_f_contrato_id_unidade_sub_rogada', 'id_unidade_sub_rogada'),
        Index('idx_f_contrato_id_fornecedor', 'id_fornecedor'),
        Index('idx_f_contrato_id_tipo_contrato', 'id_tipo_contrato'),
        Index('idx_f_contrato_id_categoria_processo', 'id_categoria_processo'),
        Index('idx_f_contrato_id_usuario', 'id_usuario'),
        Index('idx_f_contrato_id_tempo_assinatura', 'id_tempo_assinatura'),
        Index('idx_f_contrato_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_contrato_id_tempo_vigencia_inicio', 'id_tempo_vigencia_inicio'),
        Index('idx_f_contrato_id_tempo_vigencia_fim', 'id_tempo_vigencia_fim'),
        Index('idx_f_contrato_id_hora_assinatura', 'id_hora_assinatura'),
        Index('idx_f_contrato_id_hora_publicacao', 'id_hora_publicacao'),
        Index('idx_f_contrato_data_etl', 'data_etl'),
    )

    def __repr__(self):
        return (f"<FContrato(id_contrato={self.id_contrato}, processo='{self.processo}', "
                f"numero_controle_pncp='{self.numero_controle_pncp}')>")