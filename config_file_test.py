import logging
import logging.config
import uuid
import logging
from contextvars import ContextVar
from collections import defaultdict
import sys


class myLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # print('msg', msg)
        # return '[%s] %s' % (self.extra['connid'], msg), kwargs
        return REQUEST_ID.get() + ';' + msg, kwargs

REQUEST_ID = ContextVar('request_id')
REQUEST_ID.set(str(uuid.uuid1()))

simple_formatter = logging.Formatter("[%(name)s " + REQUEST_ID.get() + " %(message)s]")
# complex_formatter = logging.Formatter(
#     "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
# )


class LevelFilter(logging.Filter):
    def __init__(self, low, high):
        self._low = low
        self._high = high
        logging.Filter.__init__(self)
    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False

# new handler

class DictHandler(logging.Handler):  # Inherit from logging.Handler
    def __init__(self, log_dict):
        logging.Handler.__init__(self)
        self.log_dict = log_dict
        self.info = ' (%s line %s)'

    def emit(self, record):
        message = record.msg % record.args + self.info %(record.filename, record.lineno)
        self.log_dict[REQUEST_ID.get()].append(message)


def get_child_logger(logger_name, child_name):
    return logging.getLogger(logger_name).getChild(child_name)


if __name__ == "__main__":
    # load config file
    logging.config.fileConfig("logging.conf")
    logging.root.handlers[0].addFilter(LevelFilter(logging.DEBUG, logging.INFO))
    root_logger = logging.root
    root_logger.handlers[0].setFormatter(simple_formatter)
    parent_logger = logging.getLogger('declaration')
    log_dict = defaultdict(list)
    dict_handler = DictHandler(log_dict)
    dict_handler.setFormatter(logging.root.handlers[0].formatter)
    dict_handler.setLevel(logging.WARN)
    parent_logger.addHandler(dict_handler)
    parent_logger = myLogger(parent_logger, {'request_id': ''})  # adapter
    REQUEST_ID.set(str(uuid.uuid1()))

    parent_logger.debug("debug_parent")
    parent_logger.info("info_root")
    parent_logger.warning("warn_root")
    parent_logger.error("error_root")
    REQUEST_ID.set(str(uuid.uuid1()))

    ''' issue : ?????? ????????? ?????? ?????? ?????????(myLogger)??? ?????? ????????? ?????? ??? ???,,,  '''
    # ->get child logger return ??? ????????? ???????????? ???

    # parent_logger.name

    child_logger = get_child_logger(parent_logger.name, 'blahblah_module') #### logger.name?????? ???????????? ???
    child_logger.debug("debug_module")
    child_logger.info("info_module")
    child_logger.warning("warn_module")
    child_logger.error("error_module")


    print(log_dict)