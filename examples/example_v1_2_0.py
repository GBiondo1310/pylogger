from pylogger import general_logger

LOGGER_PATH = "example_v1_2_0"


@general_logger.log(
    info_message="Executing some code",
    success_message="Succesfylly executed",
    exceptions={
        ZeroDivisionError: "You can't divide by 0",
        TypeError: "Unsupported type for division operations",
    },
    prepend=LOGGER_PATH,
)
def my_division_function(num1, num2):
    return num1 / num2


my_division_function(2, 1)

my_division_function(2, 0)

my_division_function(2, "0")
