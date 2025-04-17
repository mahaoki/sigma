from celery import shared_task
from backend.db.session import get_raw_db
from backend.engines.checking.checking_engine import CheckingEngine
from backend.db.raw.models.control import ProcessingPeriod
from backend.control.period_control import get_or_create_period
from backend.helpers.log import log_failure
from backend.helpers.logger import get_logger

logger = get_logger("run_checking")


@shared_task(bind=True, name="backend.tasks.check.run_checking.check_publication", queue="dna")
def check_publication(self, start_date, end_date, period_id, reprocessing=False):
    db = next(get_raw_db())
    try:
        period = db.query(ProcessingPeriod).filter_by(id=period_id).first()

        if not period:
            logger.warning(f"[check_publication] Period ID {period_id} not found. Skipping.")
            return {
                "period_id": period_id,
                "type": "publication",
                "total_processed": 0,
                "skipped": True
            }
        
        engine = CheckingEngine(db, period, reprocessing)
        engine.run(endpoints=["publication"])
        db.commit()

        logger.info(f"✅ Checagem de PUBLICAÇÃO concluída para {start_date} — total: {engine.total_publications}")

        return {
            "period_id": period.id,
            "type": "publication",
            "total_processed": engine.total_publications
        }

    except Exception as e:
        db.rollback()
        log_failure(
            task_name="backend.tasks.check.run_checking.check_publication",
            message=str(e),
            context={"start_date": start_date, "end_date": end_date, "reprocessing": reprocessing}
        )
        # raise self.retry(exc=e, countdown=60)
        raise e 
    finally:
        db.close()


@shared_task(bind=True, name="backend.tasks.check.run_checking.check_update", queue="humble")
def check_update(self, start_date, end_date, period_id, reprocessing=False):
    db = next(get_raw_db())
    try:
        period = db.query(ProcessingPeriod).filter_by(id=period_id).first()
        
        if not period:
            logger.warning(f"[check_publication] Period ID {period_id} not found. Skipping.")
            return {
                "period_id": period_id,
                "type": "publication",
                "total_processed": 0,
                "skipped": True
            }
        
        engine = CheckingEngine(db, period, reprocessing)
        engine.run(endpoints=["update"])
        db.commit()

        logger.info(f"✅ Checagem de ATUALIZAÇÃO concluída para {start_date} — total: {engine.total_updates}")

        return {
            "period_id": period.id,
            "type": "update",
            "total_processed": engine.total_updates
        }

    except Exception as e:
        db.rollback()
        log_failure(
            task_name="backend.tasks.check.run_checking.check_update",
            message=str(e),
            context={"start_date": start_date, "end_date": end_date, "reprocessing": reprocessing}
        )
        # raise self.retry(exc=e, countdown=60)
        raise e 
    finally:
        db.close()
