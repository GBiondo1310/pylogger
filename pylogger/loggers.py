from loguru import logger
from datetime import datetime

from .consts import (
    LOG_FORMAT,
    GENERAL_LOGGER_ERRORS,
    GENERAL_LOGGER_INFOS,
)


class BaseLogger:
    """GeneralLogger class used to log general operations,
    all info and errors will be stored in logs/infos/infos_{datetime.now().strftime(LOG_FORMAT)}.log,
    only errors will be stored in logs/error/errors_{datetime.now()}.strftime{LOG_FORMAT}.log
    """

    def __init__(
        self,
        info_task_name: str,
        info_path: str,
        error_task_name: str,
        error_path: str,
        errors_to_info: bool = False,
    ):
        self.logger_infos = logger.bind(task=info_task_name)
        self.logger_errors = logger.bind(task=error_task_name)
        logger.add(
            info_path,
            filter=lambda record: record["extra"]["task"] == info_task_name,
        )

        logger.add(
            error_path,
            filter=lambda record: record["extra"]["task"] == error_task_name,
        )
        if errors_to_info:
            logger.add(
                info_path,
                filter=lambda record: record["extra"]["task"] == error_task_name,
            )

    def info(self, message: str, function: str) -> None:
        """Shorthand function for ``self.logger_infos.info(message)``"""
        self.logger_infos.info(f"{function}:\n: INFO : {message}\n")

    def error(self, message: str, function: str) -> None:
        """Shorthand function for ``self.logger_errors.error(message)``"""
        self.logger_errors.error(f"{function}:\n: ERROR : {message}\n")

    def success(self, message: str, function: str) -> None:
        """Shorthand function for ``self.logger_infos.success(message)``"""
        self.logger_infos.success(f"{function}:\n: SUCCESS : {message}\n")

    def status_code_success(self, status_code: int):
        self.logger_infos.success(f"Status code: [{status_code}]")

    def status_code_error(self, status_code: int):
        self.logger_errors.error(f"Status code: [{status_code}]")


general_logger = BaseLogger(
    "GInfo",
    f"{GENERAL_LOGGER_INFOS}{datetime.now().strftime(LOG_FORMAT)}.log",
    "GError",
    f"{GENERAL_LOGGER_ERRORS}{datetime.now().strftime(LOG_FORMAT)}.log",
    True,
)
