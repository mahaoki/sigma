from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DUnidadeAdministrativa(DwBase):
    __tablename__ = 'd_unidade_administrativa'

    id_unidade_administrativa = Column(Integer, primary_key=True, autoincrement=True)
    id_pncp = Column(Integer, unique=True, nullable=True)
    id_staging = Column(Integer, unique=True, nullable=True)
    codigo_unidade = Column(String(50), unique=True, nullable=True)
    nome_unidade = Column(String(255), nullable=True)

    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_localizacao = Column(Integer, ForeignKey('d_municipio.id_municipio'), nullable=True)
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=True)
    data_inclusao = Column(TIMESTAMP, nullable=True)
    data_atualizacao = Column(TIMESTAMP, nullable=True)

    localizacao = relationship("DMunicipio")
    orgao = relationship("DOrgao", back_populates='unidades_administrativas')

    contratacoes = relationship("FContratacao", foreign_keys="FContratacao.id_unidade_administrativa", back_populates="unidade_administrativa")
    contratacoes_subrogadas = relationship("FContratacao", foreign_keys="FContratacao.id_unidade_sub_rogada", back_populates="unidade_sub_rogada")

    contratos = relationship("FContrato", foreign_keys="FContrato.id_unidade_administrativa", back_populates="unidade_administrativa")
    contratos_subrogadas = relationship("FContrato", foreign_keys="FContrato.id_unidade_sub_rogada", back_populates="unidade_sub_rogada")

    termos_contrato = relationship("FTermoContrato", foreign_keys="FTermoContrato.id_unidade_administrativa", back_populates="unidade_administrativa")
    termos_contrato_subrogadas = relationship("FTermoContrato", foreign_keys="FTermoContrato.id_unidade_sub_rogada", back_populates="unidade_sub_rogada")

    atas = relationship("FAtaRegistroPreco", foreign_keys="FAtaRegistroPreco.id_unidade_administrativa", back_populates="unidade_administrativa")
    atas_subrogadas = relationship("FAtaRegistroPreco", foreign_keys="FAtaRegistroPreco.id_unidade_sub_rogada", back_populates="unidade_sub_rogada")

    __table_args__ = (
        Index('idx_d_unidade_administrativa_data_etl', 'data_etl'),
        Index('idx_d_unidade_administrativa_id_orgao', 'id_orgao'),
        Index('idx_d_unidade_administrativa_id_localizacao', 'id_localizacao'),
        Index('idx_d_unidade_administrativa_codigo', 'codigo_unidade'),
        Index('idx_d_unidade_administrativa_id_pncp', 'id_pncp'),
        Index('idx_d_unidade_administrativa_id_staging', 'id_staging'),
    )


    def __repr__(self):
        return f"<DUnidadeAdministrativa(codigo='{self.codigo_unidade}', nome='{self.nome_unidade}')>"
