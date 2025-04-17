from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from backend.database.dw.models.base import DwBase
from sqlalchemy.orm import relationship

class DOrgao(DwBase):
    __tablename__ = 'd_orgao'

    id_orgao = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20), unique=True, nullable=False)
    razao_social = Column(String(255), nullable=False)
    id_esfera = Column(Integer, ForeignKey('d_esfera.id_esfera'), nullable=False)
    id_poder = Column(Integer, ForeignKey('d_poder.id_poder'), nullable=False)
    validado = Column(Boolean, nullable=True)
    data_validacao = Column(TIMESTAMP, nullable=True)
    cnpj_ente_responsavel = Column(String(20), nullable=True)
    
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    esfera = relationship("DEsfera", backref="orgaos")
    poder = relationship("DPoder", backref="orgaos")

    contratacoes = relationship('FContratacao', foreign_keys='FContratacao.id_orgao', back_populates='orgao')
    contratacoes_subrogadas = relationship('FContratacao', foreign_keys='FContratacao.id_orgao_sub_rogado', back_populates='orgao_sub_rogado')

    contratos = relationship('FContrato', foreign_keys='FContrato.id_orgao', back_populates='orgao')
    contratos_subrogados = relationship('FContrato', foreign_keys='FContrato.id_orgao_sub_rogado', back_populates='orgao_sub_rogado')
    
    termos_contrato = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_orgao', back_populates='orgao')
    termos_contrato_subrogados = relationship('FTermoContrato', foreign_keys='FTermoContrato.id_orgao_sub_rogado', back_populates='orgao_sub_rogado')

    atas = relationship('FAtaRegistroPreco',foreign_keys='FAtaRegistroPreco.id_orgao',back_populates='orgao')
    atas_subrogadas = relationship('FAtaRegistroPreco',foreign_keys='FAtaRegistroPreco.id_orgao_sub_rogado',back_populates='orgao_sub_rogado')

    unidades_administrativas = relationship('DUnidadeAdministrativa', back_populates='orgao')
    documentos_contratacao = relationship('FDocumentoContratacao', back_populates='orgao')
    documentos_contrato = relationship('FDocumentoContrato', back_populates='orgao')
    documentos_termo = relationship('FDocumentoTermoContrato', back_populates='orgao')
    instrumentos_cobranca = relationship('FInstrumentoCobranca', back_populates='orgao')

    __table_args__ = (
        Index('idx_d_orgao_data_etl', 'data_etl'),
        Index('idx_d_orgao_id_esfera', 'id_esfera'),
        Index('idx_d_orgao_id_poder', 'id_poder'),
        Index('idx_d_orgao_cnpj_ente_responsavel', 'cnpj_ente_responsavel'),
        Index('idx_d_orgao_validado', 'validado'),
        Index('idx_d_orgao_razao_social', 'razao_social'),
    )


    def __repr__(self):
        return f"<DOrgao(cnpj='{self.cnpj}', razao_social='{self.razao_social}')>"
