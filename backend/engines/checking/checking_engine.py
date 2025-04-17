from backend.config import settings
from backend.clients.api_client import BaseApiClient
from backend.engines.checking.paginator import EndpointPaginator
from backend.control.procurement_check import save_procurement_check
from backend.control.period_control import update_period_totals
from backend.helpers.log import log_failure

class CheckingEngine:
    def __init__(self, db, period, reprocessing=False, api_client=None):
        self.db = db
        self.period = period
        self.reprocessing = reprocessing
        self.api_client = api_client or BaseApiClient(settings.API_CONSULTA)
        self.paginator = EndpointPaginator(self.api_client)

        self.total_publications = 0
        self.total_updates = 0

    def run(self, endpoints=None):
        contract_modalities = list(range(1, 15))
        default_endpoints = {
            "publication": "/v1/contratacoes/publicacao",
            "update": "/v1/contratacoes/atualizacao"
        }
        selected_endpoints = {
            action: url for action, url in default_endpoints.items()
            if not endpoints or action in endpoints
        }

        for modality_code in contract_modalities:
            for action, endpoint in selected_endpoints.items():
                records, total = self.paginator.fetch_all(
                    endpoint=endpoint,
                    params={
                        "dataInicial": self.period.start_date.strftime("%Y%m%d"),
                        "dataFinal": self.period.end_date.strftime("%Y%m%d"),
                        "codigoModalidadeContratacao": modality_code
                    }
                )

                if action == "publication":
                    self.total_publications += total
                else:
                    self.total_updates += total

                for record in records:
                    control_number = record.get("numeroControlePNCP")
                    update_date = record.get("dataAtualizacao")
                    update_date_global = record.get("dataAtualizacaoGlobal")

                    if not control_number:
                        continue

                    save_procurement_check(
                        db=self.db,
                        control_number=control_number,
                        action=action,
                        status="pending",  # ← status será resolvido depois
                        update_date=update_date,
                        update_date_global=update_date_global,
                        period=self.period
                    )

        update_period_totals(
            db=self.db,
            period_id=self.period.id,
            total_publications=self.total_publications,
            total_updates=self.total_updates
        )
