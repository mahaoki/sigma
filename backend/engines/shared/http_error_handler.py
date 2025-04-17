import re
import json
from datetime import datetime

class HttpErrorHandler:
    def __init__(self, entity_id, entity_type, logger_function):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.logger = logger_function
        self.error_counts = {
            "no_content_204": 0,
            "client_error_4xx": 0,
            "server_error_5xx": 0,
            "bad_request_400": 0,
            "unauthorized_401": 0,
            "not_found_404": 0,
            "too_many_requests_429": 0,
            "api_failures": 0
        }

    def handle_error(self, error, context=None):
        context = context or {}
        error_str = str(error)
        status_code = self._extract_status_code(error)

        context["entity_id"] = self.entity_id
        context["entity_type"] = self.entity_type

        try:
            context_str = json.dumps(context, ensure_ascii=False)
        except Exception as e:
            context_str = f"[error serializing context] {str(e)}"

        log_args = {
            "task_name": "api",
            "engine_name": "api",
            "entity_type": self.entity_type,
            "context": context_str,
        }

        if status_code == 204 or "204" in error_str or "No Content" in error_str:
            log_args["message"] = "204 - No content"
            self.logger(**log_args)
            self.error_counts["no_content_204"] += 1
            return True

        elif status_code == 400 or "400" in error_str or "Bad Request" in error_str:
            log_args["message"] = f"400 - Bad Request: {error}"
            self.logger(**log_args)
            self.error_counts["bad_request_400"] += 1
            self.error_counts["client_error_4xx"] += 1
            return True

        elif status_code == 401 or "401" in error_str or "Unauthorized" in error_str:
            log_args["message"] = "401 - Unauthorized"
            self.logger(**log_args)
            self.error_counts["unauthorized_401"] += 1
            self.error_counts["client_error_4xx"] += 1
            return True

        elif status_code == 404 or "404" in error_str or "Not Found" in error_str:
            log_args["message"] = "404 - Not found"
            self.logger(**log_args)
            self.error_counts["not_found_404"] += 1
            self.error_counts["client_error_4xx"] += 1
            return True

        elif status_code == 429 or "429" in error_str or "Too Many Requests" in error_str:
            log_args["message"] = "429 - Rate limit exceeded"
            self.logger(**log_args)
            self.error_counts["too_many_requests_429"] += 1
            self.error_counts["client_error_4xx"] += 1
            return True

        elif status_code and 500 <= status_code < 600:
            log_args["message"] = f"5xx - Server error: {error}"
            self.logger(**log_args)
            self.error_counts["server_error_5xx"] += 1
            self.error_counts["api_failures"] += 1
            return False

        else:
            log_args["message"] = f"Unexpected API error: {error}"
            self.logger(**log_args)
            self.error_counts["api_failures"] += 1
            return False

    def _extract_status_code(self, error):
        if hasattr(error, "status_code"):
            return error.status_code
        if hasattr(error, "response") and hasattr(error.response, "status_code"):
            return error.response.status_code
        error_str = str(error)
        match = re.search(r"(\d{3})", error_str)
        if match:
            return int(match.group(1))
        return None

    def get_error_counts(self):
        return self.error_counts

    def should_retry(self, error):
        status = self._extract_status_code(error)
        error_str = str(error).lower()
        if status in [429, 503, 504] or "timeout" in error_str or "connection" in error_str:
            return True
        return False
