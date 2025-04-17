from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FInstrumentoCobranca(DwBase):
    __tablename__ = 'f_instrumento_cobranca'

    id_instrumento = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=False)
    id_contrato = Column(Integer, ForeignKey('f_contrato.id_contrato'), nullable=True)
    id_nota_fiscal = Column(Integer, ForeignKey('d_nota_fiscal.id_nota_fiscal'), nullable=True)
    id_tipo_instrumento_cobranca = Column(Integer, ForeignKey('d_tipo_instrumento_cobranca.id_tipo_instrumento_cobranca'), nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    sequencial_instrumento_cobranca = Column(Integer, nullable=False)
    numero_instrumento_cobranca = Column(String(50), nullable=True)
    valor_total = Column(Numeric(15,2), nullable=True)
    observacao = Column(String(500), nullable=True)

    ano = Column(Integer, nullable=True) 
    fonte_nfe = Column(Integer, nullable=True) 
    json_response_nfe = Column(Text, nullable=True) 
    status_response_nfe = Column(String(10), nullable=True) 
    sequencial_contrato = Column(Integer, nullable=True) 

    data_emissao_documento = Column(TIMESTAMP, nullable=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True) 
    data_consulta_nfe = Column(TIMESTAMP, nullable=True)

    nota_fiscal = relationship('DNotaFiscal', back_populates='instrumentos_cobranca')
    tipo_instrumento_cobranca = relationship('DTipoInstrumentoCobranca', back_populates='instrumentos_cobranca')
    orgao = relationship('DOrgao', back_populates='instrumentos_cobranca')

    contrato = relationship('FContrato', back_populates='instrumentos_cobranca')

    __table_args__ = (
        Index('idx_f_instr_cobr_data_etl', 'data_etl'),
        Index('idx_f_instr_cobr_id_orgao', 'id_orgao'),
        Index('idx_f_instr_cobr_id_contrato', 'id_contrato'),
        Index('idx_f_instr_cobr_id_nfe', 'id_nota_fiscal'),
        Index('idx_f_instr_cobr_tipo_instr', 'id_tipo_instrumento_cobranca'),
        Index('idx_f_instr_cobr_sequencial', 'sequencial_instrumento_cobranca'),
        Index('idx_f_instr_cobr_data_emissao', 'data_emissao_documento'),
        Index('idx_f_instr_cobr_data_inclusao', 'data_inclusao'),
    )

    def __repr__(self):
        return (
            f"<FInstrumentoCobranca(id_staging={self.id_staging}, "
            f"numero='{self.numero_instrumento_cobranca}', valor={self.valor_total})>"
        )