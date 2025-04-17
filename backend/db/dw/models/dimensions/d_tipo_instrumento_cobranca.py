from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DTipoInstrumentoCobranca(DwBase):
    __tablename__ = 'd_tipo_instrumento_cobranca'

    id_tipo_instrumento_cobranca = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer, nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    status_ativo = Column(Boolean, default=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True)

    instrumentos_cobranca = relationship('FInstrumentoCobranca', back_populates='tipo_instrumento_cobranca')

    def __repr__(self):
        return f"<DTipoInstrumentoCobranca(codigo='{self.codigo}', nome='{self.nome}')>"
