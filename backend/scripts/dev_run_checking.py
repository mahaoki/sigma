# run_checking_flow.py

from backend.core.celery_app import celery
from backend.db.session import get_raw_db
from backend.control.period_control import get_or_create_period

if __name__ == "__main__":
    start_date = end_date = "2025-04-01"
    # start_date = end_date = "2025-01-04"
    reprocessing = True

    db = next(get_raw_db())
    period = get_or_create_period(db, start_date, end_date, reprocessing)
    db.close()

    task = celery.send_task(
        "backend.orchestrators.check_flow",  # <- Nome da task orquestradora
        args=[start_date, end_date, reprocessing],
        queue="dna"
    )
    print(f"✅ Orchestration task enqueued! Task ID: {task.id}")
