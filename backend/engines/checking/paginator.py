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

            print(f"🔍 Fetching: {endpoint} page={page} params={paged_params}")  # debug temporário

            response, error = self.api_client.get(endpoint, params=paged_params)

            if error:
                raise Exception(f"API error: {error}")

            if not response.get("data"):
                break

            if page == 1:
                total = response.get("totalRegistros", 0)

            all_data.extend(response["data"])
            page += 1

        return all_data, total
