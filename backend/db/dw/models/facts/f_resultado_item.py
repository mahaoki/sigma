from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, CHAR, TIMESTAMP, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FResultadoItem(DwBase):
    __tablename__ = 'f_resultado_item'

    id_resultado_item = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)

    id_item_contratacao = Column(Integer, ForeignKey('f_item_contratacao.id_item_contratacao'))
    id_fornecedor = Column(Integer, ForeignKey('d_fornecedor.id_fornecedor'))
    id_situacao_resultado = Column(Integer, ForeignKey('d_situacao_resultado.id_situacao'))
    id_motivo_cancelamento = Column(Integer, ForeignKey('d_motivo_cancelamento.id_motivo_cancelamento'))
    id_amparo_legal_criterio_desempate = Column(Integer, ForeignKey('d_amparo_legal.id_amparo_legal'), nullable=True)
    id_amparo_legal_margem_preferencia = Column(Integer, ForeignKey('d_amparo_legal.id_amparo_legal'), nullable=True)

    codigo_pais_origem_produto = Column(CHAR(3), ForeignKey('d_pais.codigo_pais'))
    codigo_moeda = Column(CHAR(3), ForeignKey('d_moeda.codigo_moeda'))
    data_atualizacao = Column(TIMESTAMP)

    sequencial_resultado = Column(Integer)
    ordem_classificacao_srp = Column(Integer)
    quantidade_homologada = Column(Numeric(15,2))
   
    valor_nominal_moeda_estrangeira = Column(Numeric(15,2))
    timezone_cotacao_moeda = Column(String(50))
    valor_unitario_homologado = Column(Numeric(15,2))
    valor_total_homologado = Column(Numeric(15,2))
    percentual_desconto = Column(Numeric(5,2))

    id_tempo_resultado = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_inclusao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_cancelamento = Column(Integer, ForeignKey('d_tempo.id_tempo'))

    id_hora_resultado = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_inclusao = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_cancelamento = Column(Integer, ForeignKey('d_hora.id_hora'))

    aplicacao_beneficio_me_epp = Column(Boolean)
    indicador_subcontratacao = Column(Boolean)
    aplicacao_criterio_desempate = Column(Boolean)
    aplicacao_margem_preferencia = Column(Boolean)

    item_contratacao = relationship('FItemContratacao', back_populates='resultados_item')
    fornecedor = relationship('DFornecedor', backref='resultados_fornecedor')

    tempo_resultado = relationship('DTempo', foreign_keys=[id_tempo_resultado], back_populates='resultados_item_resultado')
    tempo_inclusao = relationship('DTempo', foreign_keys=[id_tempo_inclusao], back_populates='resultados_item_inclusao')
    tempo_cancelamento = relationship('DTempo', foreign_keys=[id_tempo_cancelamento], back_populates='resultados_item_cancelamento')

    hora_resultado = relationship('DHora', foreign_keys=[id_hora_resultado], back_populates='resultados_item_resultado')
    hora_inclusao = relationship('DHora', foreign_keys=[id_hora_inclusao], back_populates='resultados_item_inclusao')
    hora_cancelamento = relationship('DHora', foreign_keys=[id_hora_cancelamento], back_populates='resultados_item_cancelamento')

    amparo_legal_criterio_desempate = relationship("DAmparoLegal", foreign_keys=[id_amparo_legal_criterio_desempate])
    amparo_legal_margem_preferencia = relationship("DAmparoLegal", foreign_keys=[id_amparo_legal_margem_preferencia])

    pais_origem_produto = relationship('DPais', backref='resultados_item')
    moeda = relationship('DMoeda', backref='resultados_item')

    __table_args__ = (
        Index('idx_f_resultado_item_data_etl', 'data_etl'),
        Index('idx_f_resultado_item_id_item_contratacao', 'id_item_contratacao'),
        Index('idx_f_resultado_item_id_fornecedor', 'id_fornecedor'),
        Index('idx_f_resultado_item_id_situacao_resultado', 'id_situacao_resultado'),
        Index('idx_f_resultado_item_id_motivo_cancelamento', 'id_motivo_cancelamento'),
        Index('idx_f_resultado_item_id_amparo_criterio', 'id_amparo_legal_criterio_desempate'),
        Index('idx_f_resultado_item_id_amparo_margem', 'id_amparo_legal_margem_preferencia'),
        Index('idx_f_resultado_item_codigo_pais_origem', 'codigo_pais_origem_produto'),
        Index('idx_f_resultado_item_codigo_moeda', 'codigo_moeda'),
        Index('idx_f_resultado_item_id_tempo_resultado', 'id_tempo_resultado'),
        Index('idx_f_resultado_item_id_tempo_inclusao', 'id_tempo_inclusao'),
        Index('idx_f_resultado_item_id_tempo_cancelamento', 'id_tempo_cancelamento'),
        Index('idx_f_resultado_item_id_hora_resultado', 'id_hora_resultado'),
        Index('idx_f_resultado_item_id_hora_inclusao', 'id_hora_inclusao'),
        Index('idx_f_resultado_item_id_hora_cancelamento', 'id_hora_cancelamento'),
    )

    def __repr__(self):
        return f"<FResultadoItem(id_staging={self.id_staging}, fornecedor={self.id_fornecedor}, valor={self.valor_total_homologado})>"