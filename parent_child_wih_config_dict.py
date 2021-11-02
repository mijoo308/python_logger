import logging
import logging.config

config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "[%(name)s] %(message)s %(funcName)s %(module)s %(filename)s"},
        "complex": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "formatter": "complex",
            "level": "ERROR",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "WARNING"},
    "loggers": {"declaration": {"level": "INFO"}, "declaration.drive": {"level": "DEBUG"},},
}

logging.config.dictConfig(config)


def function_name_test(logger):
    logger.error('func name 테스트')



if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.debug("디버그")
    root_logger.info("정보")
    root_logger.error("오류")

    parent_logger = logging.getLogger("declaration")
    parent_logger.debug("디버그")
    parent_logger.info("정보")
    parent_logger.error("오류")

    child_logger = logging.getLogger("declaration.drive")
    child_logger.debug("디버그")
    child_logger.info("정보")
    child_logger.error("오류")
    print('-------------------------------')
    function_name_test(child_logger)