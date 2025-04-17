from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, CHAR, Index, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FItemContratacao(DwBase):
    __tablename__ = 'f_item_contratacao'

    id_item_contratacao = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False, index=True)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_contratacao = Column(Integer, ForeignKey('f_contratacao.id_contratacao'), nullable=False, index=True)
    id_categoria_item = Column(Integer, ForeignKey('d_categoria_item.id_categoria'), nullable=True)
    id_material_servico = Column(CHAR(1), ForeignKey('d_material_servico.id_material_servico'), nullable=True)
    id_situacao_compra_item = Column(Integer, ForeignKey('d_situacao_compra_item.id_situacao_compra_item'), nullable=True)
    id_criterio_julgamento = Column(Integer, ForeignKey('d_criterio_julgamento.id_criterio_julgamento'), nullable=True)
    id_tipo_beneficio = Column(Integer, ForeignKey('d_tipo_beneficio.id_tipo_beneficio'), nullable=True)

    id_catalogo = Column(Integer, ForeignKey('d_catalogo.id_catalogo'), nullable=True)  # FK adicionada
    id_categoria_item_catalogo = Column(Integer, ForeignKey('d_categoria_item_catalogo.id_categoria_item_catalogo'), nullable=True)  # FK adicionada

    id_tempo_inclusao = Column(Integer, ForeignKey('d_tempo.id_tempo'), nullable=True)
    id_hora_inclusao = Column(Integer, ForeignKey('d_hora.id_hora'), nullable=True)

    incentivo_produtivo_basico = Column(Boolean, default=False)
    aplicabilidade_margem_pref_normal = Column(Boolean, default=False)
    aplicabilidade_margem_pref_adicional = Column(Boolean, default=False)
    orcamento_sigiloso = Column(Boolean, default=False)
    tem_resultado = Column(Boolean, default=False, index=True)

    numero_item = Column(Integer, nullable=True)
    descricao_item = Column(Text, nullable=True)
    unidade_medida = Column(String(50), nullable=True)
    quantidade = Column(Numeric(15, 2), nullable=True)
    valor_unitario_estimado = Column(Numeric(15, 2), nullable=True)
    valor_total_estimado = Column(Numeric(15, 2), nullable=True)

    data_atualizacao = Column(TIMESTAMP, nullable=True)
    imagem = Column(Integer, nullable=True)
    patrimonio = Column(Text, nullable=True)
    catalogo_codigo_item = Column(Text, nullable=True)
    informacao_complementar = Column(Text, nullable=True)
    codigo_registro_imobiliario = Column(Text, nullable=True)

    percentual_margem_pref_normal = Column(Numeric(5, 2), nullable=True)
    percentual_margem_pref_adicional = Column(Numeric(5, 2), nullable=True)

    # Relacionamentos explícitos e organizados:
    contratacao = relationship('FContratacao', back_populates='itens_contratacao')
    resultados_item = relationship('FResultadoItem', back_populates='item_contratacao')
    
    tempo_inclusao = relationship('DTempo', foreign_keys=[id_tempo_inclusao], back_populates='itens_contratacao_inclusao') 
    hora_inclusao = relationship("DHora", foreign_keys=[id_hora_inclusao], back_populates="itens_contratacao_inclusao")

    categoria_item = relationship('DCategoriaItem', backref='itens_contratacao')
    material_servico = relationship('DMaterialServico', backref='itens_contratacao')
    situacao_compra_item = relationship('DSituacaoCompraItem', backref='itens_contratacao')
    criterio_julgamento = relationship('DCriterioJulgamento', backref='itens_contratacao')
    tipo_beneficio = relationship('DTipoBeneficio', backref='itens_contratacao')

    catalogo = relationship('DCatalogo', backref='itens_contratacao')  # relacionamento explícito adicionado
    categoria_item_catalogo = relationship('DCategoriaItemCatalogo', backref='itens_contratacao')  # relacionamento explícito adicionado

    __table_args__ = (
        # Index(
        #     'ix_f_item_contratacao_descricao_item', 
        #     'descricao_item', 
        #     postgresql_using='gin', 
        #     postgresql_ops={'descricao_item': 'gin_trgm_ops'}
        # ),
        Index('idx_f_item_contratacao_numero_item', 'numero_item'),
        Index('idx_f_item_contratacao_data_etl', 'data_etl'),
        Index('idx_f_item_contratacao_tem_resultado', 'tem_resultado'),
        Index('idx_f_item_contratacao_id_categoria_item', 'id_categoria_item'),
        Index('idx_f_item_contratacao_id_material_servico', 'id_material_servico'),
        Index('idx_f_item_contratacao_id_criterio_julgamento', 'id_criterio_julgamento'),
        Index('idx_f_item_contratacao_id_tipo_beneficio', 'id_tipo_beneficio'),
        Index('idx_f_item_contratacao_id_catalogo', 'id_catalogo'),
        Index('idx_f_item_contratacao_id_categoria_item_catalogo', 'id_categoria_item_catalogo'),
    )

    def __repr__(self):
        return (f"<FItemContratacao(id_item_contratacao={self.id_item_contratacao}, "
                f"numero_item={self.numero_item}, descricao_item='{self.descricao_item[:50]}...')>")
