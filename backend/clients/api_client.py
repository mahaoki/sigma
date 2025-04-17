import requests
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from backend.config.settings import settings
from backend.helpers.log import log_failure
from backend.engines.shared.http_error_handler import HttpErrorHandler

class BaseApiClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if auth_token:
            self.headers['Authorization'] = f'Bearer {auth_token}'

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        stop=stop_after_attempt(settings.API_RETRY_ATTEMPTS),
        wait=wait_exponential(min=settings.API_RETRY_WAIT_MIN, max=settings.API_RETRY_WAIT_MAX),
        reraise=True
    )
    def get(self, endpoint, params=None, log_context=None):
        url = f"{self.base_url}{endpoint}"
        error_handler = HttpErrorHandler(log_context, "api", logger_function=log_failure)

        try:
            response = requests.get(
                url, params=params, headers=self.headers, timeout=settings.API_TIMEOUT
            )
            if response.status_code in (200, 201):
                if not response.text.strip():
                    return {}, None
                return response.json(), None
            
            elif response.status_code == 204:
                return {}, None 

            return self._handle_error(
                error_handler, log_context,
                f"HTTP error {response.status_code}",
                endpoint, response.status_code, response.text
            )

        except requests.RequestException as e:
            return self._handle_error(
                error_handler, log_context,
                f"Request failed after retries: {str(e)}",
                endpoint
            )

    def _handle_error(self, handler, log_context, msg, endpoint, status_code=None, response_raw=None):
        context = {
            "endpoint": endpoint,
            "status_code": status_code,
            "response_snippet": response_raw[:200] if response_raw else None
        }
        handler.handle_error(msg, context)
        return None, msg
