from sqlalchemy import Column, CHAR, String
from backend.database.dw.models.base import DwBase

class DMaterialServico(DwBase):
    __tablename__ = 'd_material_servico'

    id_material_servico = Column(CHAR(1), primary_key=True)  # "M" ou "S"
    nome_material_servico = Column(String(50), nullable=False)  # Material ou Serviço

    def __repr__(self):
        return f"<DMaterialServico(tipo='{self.descricao}')>"
