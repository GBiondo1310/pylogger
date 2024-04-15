# PyLogger package

# Install in editable mode:
```
pip install -e .
```

# Install from github:
```
pip install pylogger@git+"https://github.com/GBiondo1310/pylogger.git#egg=<pylogger>"
```

# How to create a new logger

```
from pylogger import BaseLogger

new_logger = BaseLogger(
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


## You could just use the general_logger included in this file:

```
from pylogger import general_logger

general_logger.info("This is an info log")
general_logger.error("This is an error log")
general_logger.success("This is a success log")
```
