from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FNotaFiscalItem(DwBase):
    __tablename__ = 'f_nota_fiscal_item'

    id_nota_fiscal_item = Column(Integer, primary_key=True, autoincrement=True)
    id_nota_fiscal = Column(Integer, ForeignKey('d_nota_fiscal.id_nota_fiscal'), nullable=False)
    id_ncm_nbs = Column(Integer, ForeignKey('d_ncm_nbs.id_ncm_nbs'), nullable=True)

    numero_item = Column(String(20), nullable=True)
    descricao_produto_servico = Column(String(500), nullable=False)
    descricao_ncm = Column(String(255), nullable=True)
    cfop = Column(String(20), nullable=True)
    quantidade = Column(Numeric(15, 3), nullable=True)
    unidade = Column(String(50), nullable=True)
    valor_unitario = Column(Numeric(15, 2), nullable=True)
    valor_total = Column(Numeric(15, 2), nullable=True)

    data_inclusao = Column(TIMESTAMP, nullable=True)

    # Relacionamentos
    nota_fiscal = relationship('DNotaFiscal', back_populates='itens')
    ncm_nbs = relationship('DNcmNbs', back_populates='itens_nfe')

    __table_args__ = (
        Index('idx_f_nf_item_id_nota_fiscal', 'id_nota_fiscal'),
        Index('idx_f_nf_item_id_ncm_nbs', 'id_ncm_nbs'),
    )

    def __repr__(self):
        return (f"<FNotaFiscalItem(descricao='{self.descricao_produto_servico}', "
                f"valor_total='{self.valor_total}')>")
