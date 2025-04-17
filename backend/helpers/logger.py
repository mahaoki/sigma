import logging

def get_logger(name: str = None):
    return logging.getLogger(name or "ColetorPNCP")
