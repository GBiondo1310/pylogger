# PyLogger package

# Install in editable mode:
```
pip install -e .
```

# Install from github:
```
pip install pylogger@git+"https://github.com/GBiondo1310/pylogger.git"
```

# New in version: 1.2.0:
### PyLogger now has decorators!
Decorators have finally been implemented to avoid redundant lines of code and to provide much cleaner implementation.
[Go to decoration usage](#how-to-use-decorators)
---

# How to create a custom logger

```
from pylogger import BaseLogger

custom_logger = BaseLogger(
    info_task_name,
    f"{info_path}{info_log_filename}.log",
    "error_task_name",
    f"{error_path}{error_log_filename}.log",
    True,
)
```

- ```info_task_name``` Is the unique name assigned to this logger for info tasks, ```str``` type and can be anything as long as it is unique and not shared by any other logger
- ```error_task_name``` Is the unique name assigned to this logger for error tasks, ```str``` type and can be anything as long as it is unique and not shared by any other logger
- ```info_path``` Is the path where the info log files will be stored, usually ```logs/infos/```
- ```error_path``` Is the path where the error log files will be stored, usually ```logs/errors/```
- ```info_log_filename``` Is the name of the info logs file, usually something that includes a date so that the next day you will have a new info logs file
- ```error_log_filename``` Is the name of the error logs file, usually something that includes a date so that the next day you will have a new error logs file
- The last parameter marked here as ```True``` is a flag which sets wether errors should also be logged in the info file. If false, errors will only be reported in the error log files

### Example:

```
from pylogger import BaseLogger
from datetime import datetime
from pylogger.consts import LOG_FORMAT

general_logger = BaseLogger(
    "GInfo",
    f"{GENERAL_LOGGER_INFOS}{datetime.now().strftime(LOG_FORMAT)}.log",
    "GError",
    f"{GENERAL_LOGGER_ERRORS}{datetime.now().strftime(LOG_FORMAT)}.log",
    True,
)
```


## You can just use the general_logger included in this file:

```
from pylogger import general_logger

general_logger.info("This is an info log")
general_logger.error("This is an error log")
general_logger.success("This is a success log")
```


## How to use decorators
(v 1.2.0)

With the ```log``` decorator, you can now define and use your function without implementing all the redundant code as in previous version.

#### Log decorato example
Being ```test.py``` the following file
```py
# Import the default logger
from pylogger import general_logger
from pylogger.exceptions import UnknownError

# Or check "How to implement a custom logger" section

#: (Best practice) Pass a variable to the "prepend" parameter of the log decorator
# so that logs displays the source of the log
log_path = "test"


@general_logger.log(
    info_message="Info message to be displayed before function execution",
    success_message="Success message to be displayed after function successful execution",
    exceptions={
        ZeroDivisionError: "Division by 0 is forbidden"
    },  # <= Put here all the exceptions that have custom log messages
    prepend=log_path,
)
def logged_divide_func(num1, num2):
    return num1 / num2


result = logged_divide_func(2, 1)
print(result)

try:
    logged_divide_func(2, 0)  # <= Has custom log message (ZeroDivisionError)
except ZeroDivisionError:  # You still need to catch Errors on your own
    print("ZeroDivisionError catched but log still displayed")

try:
    logged_divide_func(
        2, "0"
    )  # <= Has default log message (raises pylogger.exception.UnknownError by default)
except UnknownError:  # You still need to catch Errors on your own
    print("UnknownError catched but log still displayed")
```

Running ```python test.py``` will get a similar result:

```
2024-06-13 20:38:57.538 | INFO     | pylogger.loggers:info:39 - test.logged_divide_func:
: INFO : Info message to be displayed before function execution

2024-06-13 20:38:57.539 | SUCCESS  | pylogger.loggers:success:47 - test.logged_divide_func:
: SUCCESS : Success message to be displayed after function successful execution

2.0
2024-06-13 20:38:57.539 | INFO     | pylogger.loggers:info:39 - test.logged_divide_func:
: INFO : Info message to be displayed before function execution

2024-06-13 20:38:57.539 | ERROR    | pylogger.loggers:error:43 - test.logged_divide_func:
: ERROR : Division by 0 is forbidden

ZeroDivisionError catched but log still displayed
2024-06-13 20:38:57.540 | INFO     | pylogger.loggers:info:39 - test.logged_divide_func:
: INFO : Info message to be displayed before function execution

2024-06-13 20:38:57.540 | ERROR    | pylogger.loggers:error:43 - test.logged_divide_func:
: ERROR : UnknownError
Traceback (most recent call last):
  File "/home/path/to/pylogger/loggers.py", line 70, in wrapper
    result = function(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/path/to/test.py", line 21, in logged_divide_func
    return num1 / num2
           ~~~~~^~~~~~
TypeError: unsupported operand type(s) for /: 'int' and 'str'


UnknownError catched but log still displayed