"""
Helpers para criar ou atualizar períodos de checagem.

Garantias:
• Datas de entrada sempre convertidas para datetime.date (parse_date)
• Índice único (start_date, end_date) respeitado
• Transações atômicas: commit em todos os caminhos de sucesso
• Validação: datas obrigatórias; reprocessamento controlado
"""

from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from backend.db.raw.models.control import ProcessingPeriod
from backend.helpers.parsers import parse_date
from backend.helpers.log import log_failure
from backend.helpers.logger import get_logger

logger = get_logger("period_control")


# ------------------------------------------------------------------------------
# Utilitário interno
# ------------------------------------------------------------------------------
def _ensure_date(val: str | date) -> date:
    """
    Converte string YYYY‑MM‑DD em datetime.date.
    Lança ValueError se não conseguir.
    """
    d = parse_date(val)
    if d is None:
        raise ValueError(f"Invalid date: {val!r}")
    return d


# ------------------------------------------------------------------------------
# Cria ou obtém período
# ------------------------------------------------------------------------------
def get_or_create_period(db, start_date: str | date, end_date: str | date, reprocessing: bool = False) -> ProcessingPeriod:
    """
    • Se existir e reprocessing=False → retorna
    • Se não existir → cria
    • Se existir e reprocessing=True → marca como 'running' e atualiza reprocessed_at
    Sempre retorna o objeto `ProcessingPeriod` já persistido.
    """

    start_date_dt = _ensure_date(start_date)
    end_date_dt   = _ensure_date(end_date)

    try:
        period = (
            db.query(ProcessingPeriod)
              .filter_by(start_date=start_date_dt, end_date=end_date_dt)
              .first()
        )

        now = datetime.utcnow()

        if period and not reprocessing:
            logger.debug(f"[period] Reusing existing period ID {period.id}")
            return period

        if not period:
            period = ProcessingPeriod(
                start_date=start_date_dt,
                end_date=end_date_dt,
                status="running",
                started_at=now
            )
            db.add(period)
            logger.info(f"[period] New period created: {start_date_dt} to {end_date_dt}")
        else:
            period.status = "running"
            period.reprocessed_at = now
            logger.info(f"[period] Period reprocessing triggered: ID {period.id}")

        db.flush()
        db.refresh(period)
        return period

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"[period] IntegrityError on period creation: {str(e)}")
        # Outra transação inseriu o mesmo período; recupera novamente
        period = (
            db.query(ProcessingPeriod)
              .filter_by(start_date=start_date_dt, end_date=end_date_dt)
              .first()
        )
        if period:
            logger.info(f"[period] Recovered period after concurrent insert: ID {period.id}")
            return period

        log_failure(task_name="get_or_create_period", message=str(e))
        raise RuntimeError("Could not recover period after concurrent insert.")


# ------------------------------------------------------------------------------
# Atualiza totais processados
# ------------------------------------------------------------------------------
def update_period_totals(db, period_id: int, total_publications: int, total_updates: int) -> None:
    period = db.query(ProcessingPeriod).filter_by(id=period_id).first()
    if not period:
        log_failure(
            task_name="update_period_totals",
            message=f"ProcessingPeriod id={period_id} not found"
        )
        return

    period.total_checked_publications = total_publications
    period.total_checked_updates      = total_updates
    logger.info(f"[period] Totals updated: publications={total_publications}, updates={total_updates} (ID {period_id})")
    db.flush()
