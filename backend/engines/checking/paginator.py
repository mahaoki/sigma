import logging

logger = logging.getLogger(__name__)

class EndpointPaginator:
    def __init__(self, api_client):
        self.api_client = api_client

    def fetch_all(self, endpoint, params):
        all_data = []
        page = 1
        total = 0

        while True:
            paged_params = params.copy()
            paged_params["pagina"] = page
            paged_params["tamanhoPagina"] = 50  # conforme a API PNCP

            logger.warning(f"🔍 Fetching: {endpoint} page={page} params={paged_params}")

            response, error = self.api_client.get(endpoint, params=paged_params)

            if error:
                logger.error(f"❌ API error on {endpoint} — page={page} — params={paged_params} — error={error}")
                raise Exception(f"API error: {error} — endpoint={endpoint}, page={page}, params={paged_params}")

            if not response or not response.get("data"):
                logger.info(f"✅ Finished fetching: {endpoint} — total pages={page - 1} — total records={total}")
                break

            if page == 1:
                total = response.get("totalRegistros", 0)
                logger.info(f"📊 Total records reported: {total} for endpoint {endpoint}")

            all_data.extend(response["data"])
            page += 1

        return all_data, total
