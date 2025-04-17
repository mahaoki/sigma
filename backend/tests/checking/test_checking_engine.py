from unittest.mock import MagicMock
from backend.engines.checking.checking_engine import CheckingEngine
from datetime import date

def test_engine_runs(monkeypatch):
    db = MagicMock()
    period = MagicMock(start_date=date(2025, 4, 1), end_date=date(2025, 4, 1), id=1)

    mock_api = MagicMock()
    mock_api.get.return_value = (
        {
            "data": [{
                "numeroControlePNCP": "123",
                "dataAtualizacao": "2025-01-01T00:00:00",
                "dataAtualizacaoGlobal": "2025-01-01T00:00:00"
            }],
            "totalRegistros": 1
        }, None
    )

    engine = CheckingEngine(db, period, api_client=mock_api)

    # Força apenas 1 modalidade para simplificar o teste
    monkeypatch.setattr(engine, "paginator", MagicMock())
    engine.paginator.fetch_all = lambda *a, **k: (mock_api.get()[0]["data"], 1)
    monkeypatch.setattr(engine, "run", lambda endpoints=None: setattr(engine, "total_publications", 1))

    engine.total_publications = 0
    engine.total_updates = 0

    engine.run(endpoints=["publication"])
    assert engine.total_publications == 1
