import pytest
from datetime import datetime, date
from uuid import uuid4
from unittest.mock import patch

from backend.tasks.check.validate_versions import validate_procurement_versions
from backend.db.raw.models.control import ProcurementCheck, ProcessingPeriod
from backend.db.raw.models.entities.procurement import Procurement

@pytest.fixture
def period(db_session):
    period = ProcessingPeriod(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 1),
        status="test"
    )
    db_session.add(period)
    db_session.commit()
    return period

def test_validate_all_statuses(db_session, period):
    db_session.query(ProcurementCheck).delete()
    db_session.query(Procurement).delete()
    db_session.commit()

    BASE_CNPJ = "06125389000188"
    YEAR = "2025"

    suffix = str(uuid4())[:6]
    pncp_new = f"{BASE_CNPJ}-1-{suffix}/{YEAR}"
    pncp_updated = f"{BASE_CNPJ}-1-001000/{YEAR}"
    pncp_ignored = f"{BASE_CNPJ}-1-001001/{YEAR}"

    # NEW
    db_session.add(ProcurementCheck(
        pncp_control_number=pncp_new,
        period_id=period.id,
        update_date=datetime(2025, 1, 14, 10, 0),
        update_date_global=datetime(2025, 1, 14, 10, 0),
        status="pending",
        period_date=period.start_date,
        action="publication"
    ))

    # UPDATED (duplicado: publicação e atualização)
    db_session.add(ProcurementCheck(
        pncp_control_number=pncp_updated,
        period_id=period.id,
        update_date=datetime(2025, 1, 14, 10, 0),
        update_date_global=datetime(2025, 1, 14, 10, 0),
        status="pending",
        period_date=period.start_date,
        action="publication"
    ))
    db_session.add(ProcurementCheck(  # duplicado, com data mais recente
        pncp_control_number=pncp_updated,
        period_id=period.id,
        update_date=datetime(2025, 1, 14, 15, 0),
        update_date_global=datetime(2025, 1, 14, 15, 0),
        status="pending",
        period_date=period.start_date,
        action="update"
    ))
    db_session.add(Procurement(
        pncp_control_number=pncp_updated,
        update_date=datetime(2025, 1, 10, 0, 0),
        update_date_global=datetime(2025, 1, 10, 0, 0),
        raw_data={}
    ))

    # IGNORED
    db_session.add(ProcurementCheck(
        pncp_control_number=pncp_ignored,
        period_id=period.id,
        update_date=datetime(2025, 1, 10, 0, 0),
        update_date_global=datetime(2025, 1, 10, 0, 0),
        status="pending",
        period_date=period.start_date,
        action="publication"
    ))
    db_session.add(Procurement(
        pncp_control_number=pncp_ignored,
        update_date=datetime(2025, 1, 10, 0, 0),
        update_date_global=datetime(2025, 1, 10, 0, 0),
        raw_data={}
    ))

    db_session.commit()

    with patch("backend.tasks.check.validate_versions.get_raw_db", return_value=iter([db_session])):
        result = validate_procurement_versions.apply(([], period.id), throw=True).get()

    assert result["new"] == 1
    assert result["updated"] == 1
    assert result["ignored"] == 2  # um por duplicata + um por data igual

