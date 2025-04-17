from celery import Celery
from backend.config.settings import settings

celery = Celery(
    "sigma",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Definição das filas nomeadas para uso genérico
WORKER_QUEUES = {
    "dna": "dna",          # Para tarefas de checagem
    "humble": "humble",    # Para tarefas de coleta
    # "euphoria": "euphoria" # Para tarefas de ETL
}

celery.conf.update(
    task_routes={
        "backend.tasks.check.run_checking.check_publication": {"queue": WORKER_QUEUES["dna"]},
        "backend.tasks.check.run_checking.check_update": {"queue": WORKER_QUEUES["humble"]},
        "backend.tasks.check.validate_versions.validate_procurement_versions": {"queue": WORKER_QUEUES["dna"]},
        "backend.orchestrators.check_flow": {"queue": WORKER_QUEUES["humble"]},
        
        
        # "backend.tasks.etl.*": {"queue": WORKER_QUEUES["euphoria"]},
    },
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)

celery.autodiscover_tasks([
    "backend.tasks.check.run_checking.check_publication",
    "backend.tasks.check.run_checking.check_update",
    "backend.tasks.check.validate_versions.validate_procurement_versions",
    "backend.orchestrators.check_flow"
])
