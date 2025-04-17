import pytest
from datetime import date
from backend.db.raw.models.control import ProcurementCheck, ProcessingPeriod
from backend.control.procurement_check import save_procurement_check

@pytest.fixture
def period(db_session):
    p = ProcessingPeriod(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 1),
        status="test"
    )
    db_session.add(p)
    db_session.commit()
    return p

def test_save_procurement_check_creates_entry(db_session, period):
    control_number = "06125389000188-1-000063/2024"
    action = "publicacao"
    status = "new"
    update_date = "2025-01-14T00:08:30"
    update_date_global = "2025-01-14T00:08:30"

    save_procurement_check(
        db=db_session,
        control_number=control_number,
        action=action,
        status=status,
        update_date=update_date,
        update_date_global=update_date_global,
        period=period
    )

    result = db_session.query(ProcurementCheck).filter_by(
        pncp_control_number=control_number,
        period_id=period.id,
        action=action
    ).first()

    assert result is not None
    assert result.status == "new"
