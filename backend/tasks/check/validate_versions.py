from celery import shared_task
from sqlalchemy import func
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
        updated, ignored, new = 0, 0, 0

        # 1. Obtem todos os registros do período agrupados por número
        checks = db.query(ProcurementCheck).filter(
            ProcurementCheck.period_id == period_id
        ).all()

        # 2. Agrupa por pncp_control_number
        grouped = {}
        for check in checks:
            key = check.pncp_control_number
            grouped.setdefault(key, []).append(check)

        for control_number, group in grouped.items():
            # 3. Ordena para pegar o mais recente (por update_date_global > update_date)
            group.sort(key=lambda c: (c.update_date_global or c.update_date or datetime.min), reverse=True)
            main_check = group[0]  # o mais recente

            # 4. Marca os demais como "ignored"
            for other in group[1:]:
                other.status = "ignored"
                ignored += 1
                logger.debug(f"[{other.pncp_control_number}] Ignorado (duplicado mais antigo no período).")

            # 5. Verifica se existe no procurement
            procurement = db.query(Procurement).filter_by(pncp_control_number=control_number).first()

            update_date = main_check.update_date
            update_date_global = main_check.update_date_global

            if not procurement:
                main_check.status = "new"
                new += 1
                logger.debug(f"[{control_number}] NEW — não encontrado em procurement.")
                continue

            update_date_db = procurement.update_date or datetime.min
            update_date_global_db = procurement.update_date_global or datetime.min

            if (update_date and update_date > update_date_db) or \
               (update_date_global and update_date_global > update_date_global_db):
                main_check.status = "updated"
                updated += 1
                logger.debug(f"[{control_number}] UPDATED — nova data detectada.")
            else:
                main_check.status = "ignored"
                ignored += 1
                logger.debug(f"[{control_number}] IGNORED — datas iguais ou antigas.")

        db.commit()
        logger.info(f"Period {period_id}: new={new}, updated={updated}, ignored={ignored}")
        return {"new": new, "updated": updated, "ignored": ignored}

    except Exception as e:
        db.rollback()
        logger.error(f"[Period {period_id}] Error validating versions: {str(e)}")
        raise e
    finally:
        db.close()
