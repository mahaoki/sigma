from backend.engines.checking.paginator import EndpointPaginator

def test_paginator_fetch_all(monkeypatch):
    class MockApiClient:
        def get(self, endpoint, params):
            page = params["pagina"]
            if page > 3:
                return {"data": []}, None

            return {
                "data": [{"numeroControlePNCP": f"pncp-{i}"} for i in range((page-1)*1 + 1, page+1)],
                "totalRegistros": 3
            }, None


    paginator = EndpointPaginator(api_client=MockApiClient())
    result, total = paginator.fetch_all("/fake", {"pagina": 0})
    assert len(result) == 3
    assert total == 3
