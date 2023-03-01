"""Настройка логирования."""
import logging

import yaml


def setup_logger() -> None:
    """Настраивает логирование."""
    with open("log-config.yml") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
