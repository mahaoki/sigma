from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from backend.database.raw.models import (
    ControleContratacaoPNCP, ControleEtapaEntidade, ColetaLog,
    Contratacao, Item, ResultadoItem, Contrato, DocumentoContratacao,
    DocumentoContrato, TermoContrato, DocumentoTermoContrato,
    InstrumentoCobranca, AtaRegistroPreco, DocumentoAtaRegistroPreco
)
from backend.database.dw.models import (
    FContratacao, FItemContratacao, FResultadoItem, FContrato,
    FDocumentoContratacao, FDocumentoContrato, FTermoContrato,
    FDocumentoTermoContrato, FInstrumentoCobranca, FAtaRegistroPreco,
    FDocumentoAta
)
from datetime import datetime


def contar_totais_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(ControleContratacaoPNCP.numero_controle_pncp))\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_unicas_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(distinct(ControleContratacaoPNCP.numero_controle_pncp)))\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def calcular_duracao(inicio: datetime, fim: datetime) -> str:
    if not inicio or not fim:
        return "–"
    duracao = fim - inicio
    segundos = int(duracao.total_seconds())
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    return f"{horas:02}:{minutos:02}:{segundos:02}"

def contar_entidades(periodo_id: int, etapa: str, db: Session) -> int:
    return db.query(func.count(ControleEtapaEntidade.id))\
        .filter(
            ControleEtapaEntidade.periodo_id == periodo_id,
            ControleEtapaEntidade.status == "concluida",
            ControleEtapaEntidade.etapa == etapa,
        )\
        .scalar()

def contar_falhas(periodo_id: int, db: Session) -> int:
    subquery = (
        select(Contratacao.id)
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)
        .where(ControleContratacaoPNCP.periodo_id == periodo_id)
        .subquery()
    )

    return db.query(func.count(ColetaLog.id))\
        .filter(
            ColetaLog.status == "falha",
            ColetaLog.contratacao_id.in_(subquery)
        )\
        .scalar()




# Dados da Base RAW
def contar_contratacoes_raw_por_periodo(periodo_id: int, db: Session) -> int:
    subquery = (
        select(ControleContratacaoPNCP.numero_controle_pncp)
        .where(ControleContratacaoPNCP.periodo_id == periodo_id)
        .subquery()
    )

    return db.query(func.count()).select_from(Contratacao)\
        .filter(Contratacao.numero_controle_pncp.in_(subquery))\
        .scalar()

def contar_documentos_contratacao_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(DocumentoContratacao.id))\
        .join(Contratacao, DocumentoContratacao.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_itens_raw_por_periodo(periodo_id: int, db: Session) -> int:
    subquery = (
        db.query(ControleContratacaoPNCP.numero_controle_pncp)
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)
        .distinct()
        .subquery()
    )

    return db.query(func.count(Item.id))\
        .join(Contratacao, Item.contratacao_id == Contratacao.id)\
        .join(subquery, Contratacao.numero_controle_pncp == subquery.c.numero_controle_pncp)\
        .scalar()

def contar_resultados_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(ResultadoItem.id))\
        .join(Item, ResultadoItem.item_id == Item.id)\
        .join(Contratacao, Item.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_contratos_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(Contrato.id))\
        .join(Contratacao, Contrato.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_documentos_contrato_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(DocumentoContrato.id))\
        .join(Contrato, DocumentoContrato.contrato_id == Contrato.id)\
        .join(Contratacao, Contrato.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_termos_contrato_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(TermoContrato.id))\
        .join(Contrato, TermoContrato.contrato_id == Contrato.id)\
        .join(Contratacao, Contrato.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_documentos_termo_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(DocumentoTermoContrato.id))\
        .join(TermoContrato, DocumentoTermoContrato.termo_id == TermoContrato.id)\
        .join(Contrato, TermoContrato.contrato_id == Contrato.id)\
        .join(Contratacao, Contrato.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_instrumentos_cobranca_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(InstrumentoCobranca.id))\
        .join(Contrato, InstrumentoCobranca.contrato_id == Contrato.id)\
        .join(Contratacao, Contrato.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_atas_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(AtaRegistroPreco.id))\
        .join(Contratacao, AtaRegistroPreco.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()

def contar_documentos_ata_raw_por_periodo(periodo_id: int, db: Session) -> int:
    return db.query(func.count(DocumentoAtaRegistroPreco.id))\
        .join(AtaRegistroPreco, DocumentoAtaRegistroPreco.ata_id == AtaRegistroPreco.id)\
        .join(Contratacao, AtaRegistroPreco.contratacao_id == Contratacao.id)\
        .join(ControleContratacaoPNCP, Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .scalar()





# Dados da Base DW
def contar_contratacoes_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    contratacao_ids = db_raw.query(Contratacao.id)\
        .join(ControleContratacaoPNCP,
              Contratacao.numero_controle_pncp == ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .all()

    ids_staging = [row.id for row in contratacao_ids]

    if not ids_staging:
        return 0

    return db_dw.query(func.count(FContratacao.id_contratacao))\
        .filter(FContratacao.id_staging.in_(ids_staging))\
        .scalar()

def contar_documentos_contratacao_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FDocumentoContratacao.id_documento))\
        .join(FContratacao, FDocumentoContratacao.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_itens_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    numeros = (
        db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)
        .distinct()
        .all()
    )

    pncp_numeros = [n[0] for n in numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FItemContratacao.id_item_contratacao))\
        .join(FContratacao, FItemContratacao.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_resultados_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = (
        db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)
        .distinct()
        .all()
    )
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FResultadoItem.id_resultado_item))\
        .join(FItemContratacao, FResultadoItem.id_item_contratacao == FItemContratacao.id_item_contratacao)\
        .join(FContratacao, FItemContratacao.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_contratos_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = (
        db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)
        .distinct()
        .all()
    )
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FContrato.id_contrato))\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_documentos_contrato_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FDocumentoContrato.id_documento))\
        .join(FContrato, FDocumentoContrato.id_contrato == FContrato.id_contrato)\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_termos_contrato_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FTermoContrato.id_termo_contrato))\
        .join(FContrato, FTermoContrato.id_contrato == FContrato.id_contrato)\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_documentos_termo_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FDocumentoTermoContrato.id_documento))\
        .join(FTermoContrato, FDocumentoTermoContrato.id_termo_contrato == FTermoContrato.id_termo_contrato)\
        .join(FContrato, FTermoContrato.id_contrato == FContrato.id_contrato)\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_instrumentos_cobranca_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FInstrumentoCobranca.id_instrumento))\
        .join(FContrato, FInstrumentoCobranca.id_contrato == FContrato.id_contrato)\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_atas_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FAtaRegistroPreco.id_ata))\
        .join(FContratacao, FAtaRegistroPreco.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_documentos_ata_dw_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(FDocumentoAta.id_documento))\
        .join(FAtaRegistroPreco, FDocumentoAta.id_ata == FAtaRegistroPreco.id_ata)\
        .join(FContratacao, FAtaRegistroPreco.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_orgao_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(func.distinct(FContratacao.id_orgao)))\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_unidade_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(func.distinct(FContratacao.id_unidade_administrativa)))\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()


def contar_fornecedor_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(func.distinct(FContrato.id_fornecedor)))\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()

def contar_nota_fiscal_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(func.distinct(FInstrumentoCobranca.id_nota_fiscal)))\
        .join(FContrato, FInstrumentoCobranca.id_contrato == FContrato.id_contrato)\
        .join(FContratacao, FContrato.id_contratacao == FContratacao.id_contratacao)\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()


def contar_usuarios_por_periodo(periodo_id: int, db_raw: Session, db_dw: Session) -> int:
    pncp_numeros = db_raw.query(ControleContratacaoPNCP.numero_controle_pncp)\
        .filter(ControleContratacaoPNCP.periodo_id == periodo_id)\
        .distinct().all()
    pncp_numeros = [n[0] for n in pncp_numeros]

    if not pncp_numeros:
        return 0

    return db_dw.query(func.count(func.distinct(FContratacao.id_usuario)))\
        .filter(FContratacao.numero_controle_pncp.in_(pncp_numeros))\
        .scalar()
