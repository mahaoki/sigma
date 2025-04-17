def test_param_date_format():
    from datetime import date

    period = type("Period", (), {
        "start_date": date(2025, 4, 1),
        "end_date": date(2025, 4, 1)
    })()

    params = {
        "dataInicial": period.start_date.strftime("%Y%m%d"),
        "dataFinal": period.end_date.strftime("%Y%m%d"),
        "codigoModalidadeContratacao": 8
    }

    assert params["dataInicial"] == "20250401"
    assert params["dataFinal"] == "20250401"
