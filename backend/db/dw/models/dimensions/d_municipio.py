from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DMunicipio(DwBase):
    __tablename__ = 'd_municipio'

    id_municipio = Column(Integer, primary_key=True, autoincrement=True)
    nome_municipio = Column(String(150), nullable=False)
    codigo_ibge = Column(String(10), unique=True, nullable=False)

    id_uf = Column(Integer, ForeignKey('d_unidade_federativa.id_uf'), nullable=False)
    
    # Relacionamento com UF
    uf = relationship("DUnidadeFederativa", back_populates="municipios")

    # Índices adicionais para performance em filtros comuns
    __table_args__ = (
        Index('idx_nome_municipio', 'nome_municipio'),
        Index('idx_codigo_ibge', 'codigo_ibge'),
        Index('idx_id_uf', 'id_uf'),
    )

    def __repr__(self):
        return f"<DMunicipio(nome='{self.nome_municipio}', UF='{self.uf.uf_sigla}', codigo_ibge='{self.codigo_ibge}')>"
