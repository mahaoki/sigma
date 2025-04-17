from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DUnidadeFederativa(DwBase):
    __tablename__ = 'd_unidade_federativa'

    id_uf = Column(Integer, primary_key=True, autoincrement=True)
    uf_sigla = Column(String(2), unique=True, nullable=False)
    uf_nome = Column(String(100), nullable=False)
    regiao_geografica = Column(String(20), nullable=False)

    # Relacionamento com municípios
    municipios = relationship("DMunicipio", back_populates="uf")

    # Índice adicional para melhorar performance em buscas frequentes
    __table_args__ = (
        Index('idx_uf_sigla', 'uf_sigla'),
        Index('idx_regiao_geografica', 'regiao_geografica'),
    )

    def __repr__(self):
        return f"<DUnidadeFederativa(sigla='{self.uf_sigla}', nome='{self.uf_nome}', regiao='{self.regiao_geografica}')>"
