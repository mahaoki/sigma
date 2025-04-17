import os
from logging.config import dictConfig

def setup_logging():
    # 🔹 Garante que o diretório exista
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    os.makedirs(logs_dir, exist_ok=True)

    log_file_path = os.path.join(logs_dir, "app.log")

    # 🔹 Cria toda a configuração dinamicamente
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "detailed": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
                "level": "INFO"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "filename": log_file_path,
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "encoding": "utf-8",
                "level": "INFO"
            }
        },

        "root": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }

    dictConfig(logging_config)
