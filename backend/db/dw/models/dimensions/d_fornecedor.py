from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, TIMESTAMP, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DFornecedor(DwBase):
    __tablename__ = 'd_fornecedor'

    id_fornecedor = Column(Integer, primary_key=True, autoincrement=True)
    ni_fornecedor = Column(String(20), unique=True, nullable=False)
    nome_razao_social = Column(String(255), nullable=False)
    codigo_pais = Column(CHAR(3), nullable=True, default="NA")

    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_tipo_pessoa = Column(Integer, ForeignKey('d_tipo_pessoa.id_tipo_pessoa'), nullable=True)
    id_porte_fornecedor = Column(Integer, ForeignKey('d_porte_fornecedor.id_porte_fornecedor'), nullable=True)
    id_natureza_juridica = Column(Integer, ForeignKey('d_natureza_juridica.id_natureza_juridica'), nullable=True)

    # Relacionamentos
    tipo_pessoa = relationship("DTipoPessoa", back_populates="fornecedores")
    porte_fornecedor = relationship("DPorteFornecedor", back_populates="fornecedores")
    natureza_juridica = relationship("DNaturezaJuridica", back_populates="fornecedores")

    __table_args__ = (
        Index('idx_d_fornecedor_data_etl', 'data_etl'),
        Index('idx_d_fornecedor_codigo_pais', 'codigo_pais'),
        Index('idx_d_fornecedor_id_tipo_pessoa', 'id_tipo_pessoa'),
        Index('idx_d_fornecedor_id_porte', 'id_porte_fornecedor'),
        Index('idx_d_fornecedor_id_natureza', 'id_natureza_juridica'),
    )

    def __repr__(self):
        return f"<DFornecedor(nome='{self.nome_razao_social}', ni='{self.ni_fornecedor}')>"
