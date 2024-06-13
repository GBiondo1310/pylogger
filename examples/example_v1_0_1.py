from pylogger import general_logger

LOGGER_PATH = "example_v1_0_1"


def my_division_function(num1, num2):
    FUNC_PATH = "my_function"
    general_logger.info("Executing some code", f"{LOGGER_PATH}.{FUNC_PATH}")
    try:
        result = num1 / num2
        general_logger.success("Succesfully executed", f"{LOGGER_PATH}.{FUNC_PATH}")
        return result
    except ZeroDivisionError:
        general_logger.error("You cam't divide by 0", f"{LOGGER_PATH}.{FUNC_PATH}")
        raise
    except TypeError:
        general_logger.error(
            "Unsupported type for division operations", f"{LOGGER_PATH}.{FUNC_PATH}"
        )
        raise


my_division_function(2, 1)

my_division_function(2, 0)

my_division_function(2, "0")
