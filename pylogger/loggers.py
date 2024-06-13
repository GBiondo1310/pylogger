from loguru import logger
from datetime import datetime
from traceback import format_exc
from time import time


from .consts import LOG_FORMAT, GENERAL_LOGGER_ERRORS, GENERAL_LOGGER_INFOS
from .exceptions import UnknownError


class BaseLogger:
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

    def log(
        self,
        info_message="",
        success_message="",
        exceptions={},
        prepend="",
        append=None,
    ):
        """Decorator that implements logs operations around the decorated function
        Also catches exceptions with custom log messages and re-raises them to be
        catched eslewhere

        :Example:

        >>> log_path="your.package.module"
        >>> @general_logger.log(
        >>>     info_message="Before executing function"),
        >>>     success_message="After executing function"),
        >>>     exceptions={
        >>>         ZeroDivisionError: "Can not divide by 0",
        >>>         TypeError: "Unsupported operation"
        >>>     },
        >>>     prepend = log_path,
        >>> )
        >>> def logged_division(num1, num2):
        >>>     return num1 / num2
        >>>
        >>> logged_division(1, 2)
        >>> # Outputs a bunch of logs
        >>>
        >>> logged_division(1, 0)
        >>> # Outputs a bunch of logs and the custom log from catching ZeroDivisionError

        :param info_message: The message to be displayed before the decorated function's execution
        :type info_message: str
        :param success_message: The message to be displaed after the successfull decorated function's execution
        :type success_message:str
        :param exceptions: Dict containing exceptions to catch and a custom log string to display if exception is raised
        :type excetpions: dict[Exception: str]
        :param prepend: A string intended to hold the decorated function's filename e.g. "myPythonScript"
        :type prepend: str
        :param append: A stirng intended to hold the decorated function's name, can be left to None as
        log function extracts the function name onw its own
        :type: append: str

        :return: The decorated function
        :rtype: Function

        :NOTE:
        Errors are not actually catched, they are catched just to ouptut the custom log and
        then re-raised to be catched elsewhere in your code
        """

        def inner_log(function, append=append):
            if not append:
                append = function.__name__

            def wrapper(*args, **kwargs):
                try:
                    self.info(info_message, f"{prepend}.{append}")
                    result = function(*args, **kwargs)
                    self.success(success_message, f"{prepend}.{append}")
                    return result
                except Exception as e:
                    if type(e) in exceptions.keys():
                        self.error(exceptions.get(type(e)), f"{prepend}.{append}")
                        raise
                    else:
                        error_message = f"UnknownError\n{format_exc()}"
                        self.error(
                            error_message,
                            f"{prepend}.{append}",
                        )
                        raise UnknownError(error_message)

            return wrapper

        return inner_log

    def timed_log(self, info_message="", success_message="", exceptions={}, prepend=""):
        """Decorator function that does everything :func:log() does and adds a timing
        functionality over the decorated function so user can check its performance

        :param info_message: The message to be displayed before the decorated function's execution
        :type info_message: str
        :param success_message: The message to be displaed after the successfull decorated function's execution
        :type success_message:str
        :param exceptions: Dict containing exceptions to catch and a custom log string to display if exception is raised
        :type excetpions: dict[Exception: str]
        :param prepend: A string intended to hold the decorated function's filename e.g. "myPythonScript"
        :type prepend: str
        :param append: A stirng intended to hold the decorated function's name, can be left to None as
        log function extracts the function name onw its own
        :type: append: str

        :return: The decorated function
        :rtype: Function
        """

        def inner_timed(function):
            @self.log(
                info_message, success_message, exceptions, prepend, function.__name__
            )
            def wrapper(*args, **kwargs):
                start = time()
                result = function(*args, **kwargs)
                end = time()
                self.info(f"Execution took {end - start} seconds", "BaseLogger.timed")
                return result

            return wrapper

        return inner_timed


general_logger = BaseLogger(
    "GInfo",
    f"{GENERAL_LOGGER_INFOS}{datetime.now().strftime(LOG_FORMAT)}.log",
    "GError",
    f"{GENERAL_LOGGER_ERRORS}{datetime.now().strftime(LOG_FORMAT)}.log",
    True,
)


# @general_logger.timed_log(
#     info_message="Division test",
#     success_message="Success",
# )
# def divide_numbers(num1, num2):
#     return num1 / num2


# result = divide_numbers(1, 2)
# print(result)

# result = divide_numbers(8, 4)
# print(result)

# try:
#     result = divide_numbers(100, 0)
# except ZeroDivisionError:
#     print("Zero division catched")
# except Exception:
#     print("Other exception catched")


# class TestToClass:
#     @general_logger.timed_log()
#     def setup(self):
#         self.test_attr = "test_attr"


# a = TestToClass()
# a.setup()
# print(a.test_attr)
