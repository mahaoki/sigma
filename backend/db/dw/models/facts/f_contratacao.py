from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, TIMESTAMP, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class FContratacao(DwBase):
    __tablename__ = 'f_contratacao'

    id_contratacao = Column(Integer, primary_key=True, autoincrement=True)
    id_staging = Column(Integer, unique=True, nullable=False)
    data_etl = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=False, index=True)

    id_modalidade = Column(Integer, ForeignKey('d_modalidade_contratacao.id_modalidade'))
    id_modo_disputa = Column(Integer, ForeignKey('d_modo_disputa.id_modo_disputa'))
    id_amparo_legal = Column(Integer, ForeignKey('d_amparo_legal.id_amparo_legal'))
    id_tipo_instrumento_convocatorio = Column(Integer, ForeignKey('d_tipo_instrumento_convocatorio.id_tipo_instrumento_convocatorio'))
    id_status_contratacao = Column(Integer, ForeignKey('d_status_contratacao.id_status_contratacao'))
    
    id_orgao = Column(Integer, ForeignKey('d_orgao.id_orgao'))
    id_orgao_sub_rogado = Column(Integer, ForeignKey('d_orgao.id_orgao'), nullable=True)

    id_unidade_administrativa = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'))
    id_unidade_sub_rogada = Column(Integer, ForeignKey('d_unidade_administrativa.id_unidade_administrativa'), nullable=True)
    
    id_usuario = Column(Integer, ForeignKey('d_usuario.id_usuario'))

    id_tempo_publicacao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_inclusao = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_abertura_proposta = Column(Integer, ForeignKey('d_tempo.id_tempo'))
    id_tempo_encerramento_proposta = Column(Integer, ForeignKey('d_tempo.id_tempo'))

    id_hora_publicacao = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_inclusao = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_abertura_proposta = Column(Integer, ForeignKey('d_hora.id_hora'))
    id_hora_encerramento_proposta = Column(Integer, ForeignKey('d_hora.id_hora'))

    valor_total_estimado = Column(Numeric(15, 2))
    valor_total_homologado = Column(Numeric(15, 2))

    processo = Column(String(50))
    numero_compra = Column(String(50))
    objeto_compra = Column(Text)
    srp = Column(Boolean)
    numero_controle_pncp = Column(String(100), unique=True)
    link_sistema_origem = Column(Text)

    data_atualizacao = Column(TIMESTAMP)
    data_atualizacao_global = Column(TIMESTAMP)

    ano_compra = Column(Integer)
    sequencial_compra = Column(Integer)
    informacao_complementar = Column(Text)
    link_processo_eletronico = Column(Text)
    justificativa_presencial = Column(Text)
    
    modalidade = relationship("DModalidadeContratacao")
    modo_disputa = relationship("DModoDisputa")
    amparo_legal = relationship("DAmparoLegal")
    tipo_instrumento_convocatorio = relationship("DTipoInstrumentoConvocatorio")
    status_contratacao = relationship("DStatusContratacao", back_populates="contratacoes")
    usuario = relationship("DUsuario")
    
    itens_contratacao = relationship('FItemContratacao', back_populates='contratacao')
    
    orgao = relationship("DOrgao", foreign_keys=[id_orgao], back_populates="contratacoes")
    orgao_sub_rogado = relationship("DOrgao", foreign_keys=[id_orgao_sub_rogado])

    documentos_contratacao = relationship('FDocumentoContratacao', back_populates='contratacao', cascade="all, delete-orphan", passive_deletes=True)
    contratos = relationship('FContrato', back_populates='contratacao', cascade="all, delete-orphan", passive_deletes=True, foreign_keys='FContrato.id_contratacao')
    atas = relationship('FAtaRegistroPreco', back_populates='contratacao', cascade="all, delete-orphan", passive_deletes=True, foreign_keys='FAtaRegistroPreco.id_contratacao')

    unidade_administrativa = relationship("DUnidadeAdministrativa", foreign_keys=[id_unidade_administrativa], back_populates="contratacoes")
    unidade_sub_rogada = relationship("DUnidadeAdministrativa", foreign_keys=[id_unidade_sub_rogada])

    tempo_publicacao = relationship("DTempo", foreign_keys=[id_tempo_publicacao], back_populates="contratacoes_publicacao")
    tempo_inclusao = relationship("DTempo", foreign_keys=[id_tempo_inclusao], back_populates="contratacoes_inclusao")
    tempo_abertura_proposta = relationship("DTempo", foreign_keys=[id_tempo_abertura_proposta], back_populates="contratacoes_abertura_proposta")
    tempo_encerramento_proposta = relationship("DTempo", foreign_keys=[id_tempo_encerramento_proposta], back_populates="contratacoes_encerramento_proposta")

    hora_inclusao = relationship("DHora", foreign_keys=[id_hora_inclusao], back_populates="contratacoes_inclusao")
    hora_publicacao = relationship("DHora", foreign_keys=[id_hora_publicacao], back_populates="contratacoes_publicacao")
    hora_abertura_proposta = relationship("DHora", foreign_keys=[id_hora_abertura_proposta], back_populates="contratacoes_abertura_proposta")
    hora_encerramento_proposta = relationship("DHora", foreign_keys=[id_hora_encerramento_proposta], back_populates="contratacoes_encerramento_proposta")

    __table_args__ = (
        Index('idx_f_contratacao_id_orgao', 'id_orgao'),
        Index('idx_f_contratacao_id_unidade_adm', 'id_unidade_administrativa'),
        Index('idx_f_contratacao_id_modalidade', 'id_modalidade'),
        Index('idx_f_contratacao_id_modo_disputa', 'id_modo_disputa'),
        Index('idx_f_contratacao_id_amparo_legal', 'id_amparo_legal'),
        Index('idx_f_contratacao_id_tipo_instrumento_convocatorio', 'id_tipo_instrumento_convocatorio'),
        Index('idx_f_contratacao_id_status_contratacao', 'id_status_contratacao'),
        Index('idx_f_contratacao_id_usuario', 'id_usuario'),
        Index('idx_f_contratacao_id_tempo_publicacao', 'id_tempo_publicacao'),
        Index('idx_f_contratacao_id_tempo_inclusao', 'id_tempo_inclusao'),
        Index('idx_f_contratacao_numero_controle_pncp', 'numero_controle_pncp'),
        Index('idx_f_contratacao_id_orgao_sub_rogado', 'id_orgao_sub_rogado'),
        Index('idx_f_contratacao_id_unidade_sub_rogada', 'id_unidade_sub_rogada'),
        Index('idx_f_contratacao_data_etl', 'data_etl'),
    )

    def __repr__(self):
        return f"<FContratacao(numero_controle_pncp='{self.numero_controle_pncp}', valor_estimado={self.valor_total_estimado})>"
    

