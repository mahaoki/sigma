from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DTipoPessoa(DwBase):
    __tablename__ = 'd_tipo_pessoa'

    id_tipo_pessoa = Column(Integer, primary_key=True, autoincrement=True)
    codigo_tipo_pessoa = Column(String(2), unique=True, nullable=False)  # Ex.: 'PJ', 'PF', 'NA'
    descricao = Column(String(50), nullable=False)  # Ex.: 'Pessoa Jurídica', 'Pessoa Física', 'Não Informado'

    # Relacionamento reverso para fornecedores
    fornecedores = relationship("DFornecedor", back_populates="tipo_pessoa")

    def __repr__(self):
        return f"<DTipoPessoa(codigo='{self.codigo_tipo_pessoa}', descricao='{self.descricao}')>"
