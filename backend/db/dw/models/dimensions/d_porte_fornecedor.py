from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DPorteFornecedor(DwBase):
    __tablename__ = 'd_porte_fornecedor'

    id_porte_fornecedor = Column(Integer, primary_key=True, autoincrement=True)
    porte_codigo = Column(Integer, unique=True, nullable=False)
    nome_porte = Column(String(50), nullable=False)

    # Relacionamento reverso para fornecedores
    fornecedores = relationship("DFornecedor", back_populates="porte_fornecedor")

    def __repr__(self):
        return f"<DPorteFornecedor(codigo='{self.porte_codigo}', nome='{self.nome_porte}')>"
