from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database.settings import get_raw_db, get_dw_db
from backend.database.dw.models.facts import (
    FContratacao, FDocumentoContratacao, FItemContratacao, FResultadoItem,
    FContrato, FDocumentoContrato, FTermoContrato, FDocumentoTermoContrato, 
    FInstrumentoCobranca, FAtaRegistroPreco, FDocumentoAta,
)
from backend.database.dw.models.dimensions import (
    DOrgao, DUnidadeAdministrativa, DFornecedor,
    DUsuario, DNotaFiscal,
)
from backend.database.raw.models import (
    ControleContratacaoPNCP, PeriodoColetado, ControleEtapaEntidade
)
from backend.src.collect.tasks.contratacoes import coletar_contratacoes
from backend.src.utils.helpers import format_date_api
from backend.api.v1.processamento.helpers import (
    contar_totais_por_periodo, contar_unicas_por_periodo, contar_entidades, calcular_duracao, contar_falhas,
    contar_contratacoes_raw_por_periodo, contar_contratacoes_dw_por_periodo, 
    contar_documentos_contratacao_raw_por_periodo,  contar_documentos_contratacao_dw_por_periodo,
    contar_itens_raw_por_periodo, contar_itens_dw_por_periodo, 
    contar_resultados_raw_por_periodo, contar_resultados_dw_por_periodo, 
    contar_contratos_raw_por_periodo, contar_contratos_dw_por_periodo,
    contar_documentos_contrato_raw_por_periodo, contar_documentos_contrato_dw_por_periodo,
    contar_termos_contrato_raw_por_periodo, contar_termos_contrato_dw_por_periodo,
    contar_documentos_termo_raw_por_periodo, contar_documentos_termo_dw_por_periodo,
    contar_instrumentos_cobranca_raw_por_periodo, contar_instrumentos_cobranca_dw_por_periodo,
    contar_atas_raw_por_periodo, contar_atas_dw_por_periodo,
    contar_documentos_ata_raw_por_periodo, contar_documentos_ata_dw_por_periodo,
    contar_orgao_por_periodo, contar_unidade_por_periodo, contar_nota_fiscal_por_periodo, 
    contar_fornecedor_por_periodo, contar_usuarios_por_periodo
)
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ProcessamentoRequest(BaseModel):
    data_processamento: str  # ISO 8601 format

@router.post("/iniciar")
def iniciar_processamento(payload: ProcessamentoRequest, db: Session = Depends(get_raw_db)):
    try:
        data_processamento = datetime.fromisoformat(payload.data_processamento).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Datas em formato inválido. Use ISO 8601 (ex: 2025-04-10)")

    data_processamento_fmt = format_date_api(data_processamento)

    periodo = PeriodoColetado(
        data_inicial=data_processamento_fmt,
        data_final=data_processamento_fmt,
        status="pendente",
        data_processamento=datetime.now(timezone.utc)
    )
    db.add(periodo)
    db.commit()
    db.refresh(periodo)

    coletar_contratacoes.delay(
        data_inicial=data_processamento_fmt,
        data_final=data_processamento_fmt,
        periodo_id=periodo.id
    )

    logger.info(f"[Processamento] Coleta iniciada para {data_processamento_fmt}, ID: {periodo.id}")
    return {"mensagem": "Processamento iniciado com sucesso", "periodo_id": periodo.id}


@router.get("/periodos")
def listar_periodos(
    db_raw: Session = Depends(get_raw_db),
    db_dw: Session = Depends(get_dw_db),
):
    periodos = db_raw.query(PeriodoColetado)\
        .order_by(PeriodoColetado.data_processamento.desc())\
        .limit(20).all()

    resultado = []

    for p in periodos:
        resultado.append({
            "id": p.id,
            "data": p.data_inicial.strftime("%Y-%m-%d"),
            "status": p.status,
            "inicio": p.data_processamento.isoformat() if p.data_processamento else None,
            "fim": p.data_fim_processamento.isoformat() if p.data_fim_processamento else None,
            "duracao": calcular_duracao(p.data_processamento, p.data_fim_processamento),
            "totais": contar_totais_por_periodo(p.id, db_raw) or 0,
            "unicas": contar_unicas_por_periodo(p.id, db_raw) or 0,
            "contratacoes_raw": contar_contratacoes_raw_por_periodo(p.id, db_raw) or 0,
            "entidades_raw": contar_entidades(p.id, etapa="coleta", db=db_raw) or 0,
            "contratacoes_dw": contar_contratacoes_dw_por_periodo(p.id, db_raw, db_dw) or 0,
            "falhas": contar_falhas(p.id, db_raw) or 0,            
        })

    return resultado

@router.get("/{periodo_id}/progresso")
def progresso_processamento(
    periodo_id: int,
    db_raw: Session = Depends(get_raw_db),
    db_dw: Session = Depends(get_dw_db)
):
    # Total de códigos PNCP identificados na API (verificadas)

    return {
        "totais": contar_totais_por_periodo(periodo_id, db_raw) or 0,
        "unicas": contar_unicas_por_periodo(periodo_id, db_raw) or 0,
        "contratacoes_raw": contar_contratacoes_raw_por_periodo(periodo_id, db_raw) or 0,
        "contratacoes_dw": contar_contratacoes_raw_por_periodo(periodo_id, db_raw) or 0,
    }


@router.get("/{periodo_id}/resumo")
def resumo_processamento(
    periodo_id: int,
    db_raw: Session = Depends(get_raw_db),
    db_dw: Session = Depends(get_dw_db)
):
    # 4. Entidades processadas
    entidades = [
        {"nome": "Contratações", "coleta": contar_contratacoes_raw_por_periodo(periodo_id, db_raw), "etl": contar_contratacoes_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Documentos da contratação", "coleta": contar_documentos_contratacao_raw_por_periodo(periodo_id, db_raw), "etl": contar_documentos_contratacao_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Itens", "coleta": contar_itens_raw_por_periodo(periodo_id, db_raw), "etl": contar_itens_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Resultados", "coleta": contar_resultados_raw_por_periodo(periodo_id, db_raw), "etl": contar_resultados_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Contratos", "coleta": contar_contratos_raw_por_periodo(periodo_id, db_raw), "etl": contar_contratos_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Documentos do contrato", "coleta": contar_documentos_contrato_raw_por_periodo(periodo_id, db_raw), "etl": contar_documentos_contrato_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Termos do contrato", "coleta": contar_termos_contrato_raw_por_periodo(periodo_id, db_raw), "etl": contar_termos_contrato_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Documentos do termo", "coleta": contar_documentos_termo_raw_por_periodo(periodo_id, db_raw), "etl": contar_documentos_termo_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Instrumentos de cobrança", "coleta": contar_instrumentos_cobranca_raw_por_periodo(periodo_id, db_raw), "etl": contar_instrumentos_cobranca_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Atas", "coleta": contar_atas_raw_por_periodo(periodo_id, db_raw), "etl": contar_atas_dw_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Documentos da ata", "coleta": contar_documentos_ata_raw_por_periodo(periodo_id, db_raw), "etl": contar_documentos_ata_dw_por_periodo(periodo_id, db_raw, db_dw)},
    ]

    # 5. Dimensões principais
    dimensoes = [
        {"nome": "Órgãos", "valor": contar_orgao_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Unidades administrativas", "valor": contar_unidade_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Fornecedores", "valor": contar_fornecedor_por_periodo(periodo_id, db_raw, db_dw)},
        {"nome": "Notas fiscais", "valor": contar_nota_fiscal_por_periodo(periodo_id, db_raw, db_dw)},
        # Se "Usuários" for uma dimensão adicional:
        # {"nome": "Usuários", "valor": contar_d_usuario_por_periodo(periodo_id, db_raw, db_dw)},
    ]

    return {
        "entidades": entidades,
        "dimensoes": dimensoes
    }
