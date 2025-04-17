from celery import shared_task
from backend.db.session import get_raw_db
from backend.db.raw.models.control import ProcurementCheck
from backend.db.raw.models import Procurement
from backend.helpers.logger import get_logger
from datetime import datetime

logger = get_logger("validate_versions")

@shared_task(bind=True, name="backend.tasks.check.validate_versions.validate_procurement_versions", queue="dna")
def validate_procurement_versions(self, _results, period_id: int):
    db = next(get_raw_db())
    try:
        checks = db.query(ProcurementCheck).filter(
            ProcurementCheck.period_id == period_id
        ).all()

        updated, ignored, new = 0, 0, 0

        for check in checks:
            control_number = check.pncp_control_number
            update_date = check.update_date
            update_date_global = check.update_date_global

            procurement = db.query(Procurement).filter_by(pncp_control_number=control_number).first()

            if not procurement:
                check.status = "new"
                new += 1
                logger.debug(f"[{control_number}] Novo — não encontrado em procurement.")
                continue

            update_date_db = procurement.update_date or datetime.min
            update_date_global_db = procurement.update_date_global or datetime.min

            if (update_date and update_date > update_date_db) or \
            (update_date_global and update_date_global > update_date_global_db):
                check.status = "updated"
                updated += 1
                logger.debug(f"[{control_number}] Atualizado — nova data detectada.")
            else:
                check.status = "ignored"
                ignored += 1
                logger.debug(f"[{control_number}] Ignorado — datas iguais ou antigas.")

        db.commit()
        logger.info(f"Period {period_id}: new={new}, updated={updated}, ignored={ignored}")
        return {"new": new, "updated": updated, "ignored": ignored}

    except Exception as e:
        db.rollback()
        logger.error(f"[Period {period_id}] Error validating versions: {str(e)}")
        raise e
    finally:
        db.close()
