from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, JSON, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DNotaFiscal(DwBase):
    __tablename__ = 'd_nota_fiscal'

    id_nota_fiscal = Column(Integer, primary_key=True, autoincrement=True)

    # Identificação da NF-e
    chave_nfe = Column(String(50), unique=True, nullable=False, index=True)
    numero = Column(Integer, nullable=True)
    serie = Column(Integer, nullable=True)

    # Datas importantes
    data_emissao = Column(TIMESTAMP, nullable=True)
    data_tipo_evento_mais_recente = Column(TIMESTAMP, nullable=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True)

    # Valores monetários
    valor_nota_fiscal = Column(Numeric(20, 2), nullable=True)

    # Dados Emitente
    ni_emitente = Column(String(20), nullable=True, index=True)
    nome_emitente = Column(String(255), nullable=True)
    municipio_emitente = Column(String(100), nullable=True)

    # Dados Destinatário
    codigo_orgao_destinatario = Column(String(50), nullable=True)
    nome_orgao_destinatario = Column(String(255), nullable=True)
    codigo_orgao_superior_destinatario = Column(String(50), nullable=True)
    nome_orgao_superior_destinatario = Column(String(255), nullable=True)

    # Eventos e Status
    tipo_evento_mais_recente = Column(String(100), nullable=True)
    status_response_nfe = Column(String(20), nullable=True)
    json_response_nfe = Column(JSON, nullable=True)

    # Relacionamentos
    instrumentos_cobranca = relationship('FInstrumentoCobranca', back_populates='nota_fiscal')
    itens = relationship('FNotaFiscalItem', back_populates='nota_fiscal')
    eventos = relationship('FNotaFiscalEvento', back_populates='nota_fiscal')

    __table_args__ = (
        Index('idx_d_nota_fiscal_chave_nfe', 'chave_nfe'),
        Index('idx_d_nota_fiscal_ni_emitente', 'ni_emitente'),
        Index('idx_d_nota_fiscal_data_emissao', 'data_emissao'),
    )

    def __repr__(self):
        return f"<DNotaFiscal(chave_nfe='{self.chave_nfe}', numero='{self.numero}', serie='{self.serie}')>"
