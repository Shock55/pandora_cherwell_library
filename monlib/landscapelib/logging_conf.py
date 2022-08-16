conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] [%(process)d] [%(levelname)-s] [%(name)-s] [%(funcName)-s] [%(message)s]"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "/var/log/monlib.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "/var/log/panodralib/error-logdistribute.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "warning_file_handler": {
          "class": "logging.handlers.RotatingFileHandler",
          "level": "WARNING",
          "formatter": "simple",
          "filename": "/var/log/panodralib/warning-logdistribute.log",
          "maxBytes": 10485760,
          "backupCount": 20,
          "encoding": "utf8"
      }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "info_file_handler"
        ]
    }
}
