from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DTempo(DwBase):
    __tablename__ = 'd_tempo'

    id_tempo = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, unique=True, nullable=False)
    dia = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)
    semestre = Column(Integer, nullable=False)
    dia_semana = Column(Integer, nullable=False)

    # Relacionamentos com tabelas fato
    contratacoes_publicacao = relationship('FContratacao', foreign_keys='FContratacao.id_tempo_publicacao', back_populates='tempo_publicacao')
    contratacoes_inclusao = relationship('FContratacao', foreign_keys='FContratacao.id_tempo_inclusao', back_populates='tempo_inclusao')
    contratacoes_abertura_proposta = relationship('FContratacao', foreign_keys='FContratacao.id_tempo_abertura_proposta', back_populates='tempo_abertura_proposta')
    contratacoes_encerramento_proposta = relationship('FContratacao', foreign_keys='FContratacao.id_tempo_encerramento_proposta', back_populates='tempo_encerramento_proposta')

    itens_contratacao_inclusao = relationship('FItemContratacao', foreign_keys='FItemContratacao.id_tempo_inclusao', back_populates='tempo_inclusao')

    resultados_item_resultado = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_tempo_resultado', back_populates='tempo_resultado')
    resultados_item_inclusao = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_tempo_inclusao', back_populates='tempo_inclusao')
    resultados_item_cancelamento = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_tempo_cancelamento', back_populates='tempo_cancelamento')

    contratos_assinatura = relationship('FContrato', foreign_keys='FContrato.id_tempo_assinatura', back_populates='tempo_assinatura')
    contratos_publicacao = relationship('FContrato', foreign_keys='FContrato.id_tempo_publicacao', back_populates='tempo_publicacao')
    contratos_vigencia_inicio = relationship('FContrato', foreign_keys='FContrato.id_tempo_vigencia_inicio', back_populates='tempo_vigencia_inicio')
    contratos_vigencia_fim = relationship('FContrato', foreign_keys='FContrato.id_tempo_vigencia_fim', back_populates='tempo_vigencia_fim')

    termos_contrato_assinatura = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_tempo_assinatura', back_populates='tempo_assinatura')
    termos_contrato_inclusao = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_tempo_inclusao', back_populates='tempo_inclusao')
    termos_contrato_publicacao = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_tempo_publicacao', back_populates='tempo_publicacao')
    termos_contrato_vigencia_inicio = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_tempo_vigencia_inicio', back_populates='tempo_vigencia_inicio')
    termos_contrato_vigencia_fim = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_tempo_vigencia_fim', back_populates='tempo_vigencia_fim')

    documentos_contratacao_publicacao = relationship('FDocumentoContratacao', foreign_keys='FDocumentoContratacao.id_tempo_publicacao', back_populates='tempo_publicacao')
    documentos_termo_contrato_publicacao = relationship('FDocumentoTermoContrato', foreign_keys='FDocumentoTermoContrato.id_tempo_publicacao', back_populates='tempo_publicacao')

    documentos_ata_publicacao = relationship('FDocumentoAta', foreign_keys='FDocumentoAta.id_tempo_publicacao', back_populates='tempo_publicacao')
    documentos_contrato_publicacao = relationship('FDocumentoContrato', foreign_keys='FDocumentoContrato.id_tempo_publicacao', back_populates='tempo_publicacao')

    atas_inclusao = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_inclusao', back_populates='tempo_inclusao')
    atas_assinatura = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_assinatura', back_populates='tempo_assinatura')
    atas_vigencia_inicio = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_vigencia_inicio', back_populates='tempo_vigencia_inicio')
    atas_vigencia_fim = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_vigencia_fim', back_populates='tempo_vigencia_fim')
    atas_cancelamento = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_cancelamento', back_populates='tempo_cancelamento')
    atas_publicacao = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_tempo_publicacao', back_populates='tempo_publicacao')