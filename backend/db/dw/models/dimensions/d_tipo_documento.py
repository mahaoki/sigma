from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.database.dw.models.base import DwBase

class DTipoDocumento(DwBase):
    __tablename__ = 'd_tipo_documento'

    id_tipo_documento = Column(Integer, primary_key=True)
    codigo_tipo_documento = Column(Integer, unique=True, nullable=False)
    nome_tipo_documento = Column(String(150), nullable=False)
    descricao_tipo_documento = Column(Text, nullable=True)

    documentos_contratacao = relationship('FDocumentoContratacao', back_populates='tipo_documento')
    documentos_termo = relationship('FDocumentoTermoContrato', back_populates='tipo_documento')


    def __repr__(self):
        return f"<DTipoDocumento(codigo='{self.codigo_tipo_documento}', nome='{self.nome_tipo_documento}')>"
