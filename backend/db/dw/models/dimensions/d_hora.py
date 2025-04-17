from sqlalchemy import Column, Integer, Time, String, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DHora(DwBase):
    __tablename__ = 'd_hora'

    id_hora = Column(Integer, primary_key=True, autoincrement=True)
    hora_completa = Column(Time, unique=True, nullable=False)
    hora = Column(Integer, nullable=False)
    minuto = Column(Integer, nullable=False)
    segundo = Column(Integer, nullable=False)
    periodo_dia = Column(String(20), nullable=False)

    contratacoes_inclusao = relationship('FContratacao', foreign_keys='FContratacao.id_hora_inclusao', back_populates='hora_inclusao')
    contratacoes_publicacao = relationship('FContratacao', foreign_keys='FContratacao.id_hora_publicacao', back_populates='hora_publicacao')
    contratacoes_abertura_proposta = relationship('FContratacao', foreign_keys='FContratacao.id_hora_abertura_proposta', back_populates='hora_abertura_proposta')
    contratacoes_encerramento_proposta = relationship('FContratacao', foreign_keys='FContratacao.id_hora_encerramento_proposta', back_populates='hora_encerramento_proposta')

    itens_contratacao_inclusao = relationship('FItemContratacao', foreign_keys='FItemContratacao.id_hora_inclusao', back_populates='hora_inclusao')

    documentos_contratacao_publicacao = relationship('FDocumentoContratacao', foreign_keys='FDocumentoContratacao.id_hora_publicacao', back_populates='hora_publicacao')
    documentos_termo_contrato_publicacao = relationship('FDocumentoTermoContrato', foreign_keys='FDocumentoTermoContrato.id_hora_publicacao', back_populates='hora_publicacao')
    documentos_ata_publicacao = relationship('FDocumentoAta', foreign_keys='FDocumentoAta.id_hora_publicacao', back_populates='hora_publicacao')
    documentos_contrato_publicacao = relationship('FDocumentoContrato', foreign_keys='FDocumentoContrato.id_hora_publicacao', back_populates='hora_publicacao')

    contratos_assinatura = relationship('FContrato', foreign_keys='FContrato.id_hora_assinatura', back_populates='hora_assinatura')
    contratos_publicacao = relationship('FContrato', foreign_keys='FContrato.id_hora_publicacao', back_populates='hora_publicacao')

    termos_contrato_assinatura = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_hora_assinatura', back_populates='hora_assinatura')
    termos_contrato_inclusao = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_hora_inclusao', back_populates='hora_inclusao')
    termos_contrato_publicacao = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_hora_publicacao', back_populates='hora_publicacao')

    atas_inclusao = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_hora_inclusao', back_populates='hora_inclusao')
    atas_assinatura = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_hora_assinatura', back_populates='hora_assinatura')
    atas_publicacao = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_hora_publicacao', back_populates='hora_publicacao')
    atas_cancelamento = relationship('FAtaRegistroPreco', foreign_keys='FAtaRegistroPreco.id_hora_cancelamento', back_populates='hora_cancelamento')

    resultados_item_resultado = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_hora_resultado', back_populates='hora_resultado')
    resultados_item_inclusao = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_hora_inclusao', back_populates='hora_inclusao')
    resultados_item_cancelamento = relationship('FResultadoItem', foreign_keys='FResultadoItem.id_hora_cancelamento', back_populates='hora_cancelamento')

    __table_args__ = (
        Index('idx_d_hora_periodo_dia', 'periodo_dia'),
    )

    def __repr__(self):
        return f"<DHora(hora='{self.hora_completa}', periodo='{self.periodo_dia}')>"
