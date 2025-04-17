from celery import chord
from celery import shared_task
from backend.tasks.check.run_checking import check_publication, check_update
from backend.tasks.check.validate_versions import validate_procurement_versions
from backend.control.period_control import get_or_create_period
from backend.db.session import get_raw_db
from backend.helpers.logger import get_logger

logger = get_logger("check_flow")

@shared_task(bind=True, name="backend.orchestrators.check_flow", queue="humble")
def check_flow(self, start_date: str, end_date: str, reprocessing: bool = False):
    db = next(get_raw_db())
    try:
        period = get_or_create_period(db, start_date, end_date, reprocessing)
        period_id = period.id
        db.commit()

        logger.info(f"📦 Orquestração iniciada para período ID {period_id}")

    
        chord([
            check_publication.s(start_date, end_date, period_id, reprocessing),
            check_update.s(start_date, end_date, period_id, reprocessing),
        ])(validate_procurement_versions.s(period_id))

        return {"period_id": period_id, "status": "orquestracao_enfileirada"}

    except Exception as e:
        logger.error(f"Erro na orquestração do período {start_date}: {str(e)}")
        raise e
