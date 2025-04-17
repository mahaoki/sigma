from backend.db.raw.models.control import ProcurementCheck
from backend.helpers.parsers import parse_datetime

def save_procurement_check(db, control_number, action, status, update_date, update_date_global, period):
    """
    Salva ou atualiza um registro de ProcurementCheck de forma idempotente.
    Garante que o par (control_number, action, period_date) seja único.
    """
    existing = db.query(ProcurementCheck).filter_by(
        pncp_control_number=control_number,
        action=action,
        period_date=period.start_date
    ).first()

    if existing:
        existing.update_date = parse_datetime(update_date)
        existing.update_date_global = parse_datetime(update_date_global)
        existing.status = status
    else:
        check = ProcurementCheck(
            pncp_control_number=control_number,
            action=action,
            status=status,
            update_date=parse_datetime(update_date),
            update_date_global=parse_datetime(update_date_global),
            period_id=period.id,
            period_date=period.start_date
        )
        db.add(check)
