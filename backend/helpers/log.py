"""
Grava falha crítica isoladamente no banco de dados (tabela ExecutionFailure).

Esse log é 100% isolado da transação principal da task:
- Sempre usa uma nova sessão (`SessionRaw`)
- Sempre faz commit próprio
- Nunca propaga exceção
"""

import json
from datetime import datetime, timezone
from backend.db.session import SessionRaw
from backend.db.raw.models.control import ExecutionFailure


def log_failure(
    *,
    task_name: str,
    message: str,
    context: dict | str | None = None,
    engine_name: str | None = None,
    entity_type: str | None = None,
    entity_id: int | str | None = None,
    traceback: str | None = None
):
    # 🎯 1. Serializa o contexto com fallback seguro
    if isinstance(context, dict):
        try:
            context_str = json.dumps(context, ensure_ascii=False)
        except Exception as e:
            context_str = f"[ERROR] Context could not be serialized: {str(e)}"
    else:
        context_str = str(context) if context else None

    # 🎯 2. Garante que o entity_id é inteiro ou None
    if not isinstance(entity_id, int):
        try:
            entity_id = int(entity_id)
        except (ValueError, TypeError):
            entity_id = None

    try:
        db = SessionRaw()
        failure = ExecutionFailure(
            task_name=task_name,
            engine_name=engine_name or "engine",
            entity_type=entity_type or "unknown",
            entity_id=entity_id,
            message=message,
            context=context_str,
            traceback=traceback,
            created_at=datetime.now(timezone.utc)
        )
        db.add(failure)
        db.commit()
    except Exception as e:
        print(f"[log_failure] Failed to save log: {e}")
        db.rollback()
    finally:
        db.close()
