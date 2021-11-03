import logging
import logging.config
import uuid
import logging
from contextvars import ContextVar
from collections import defaultdict


class myLogger(logging.LoggerAdapter):
    def process(self,msg,kwargs):
        return '%s' % (msg)  ,kwargs

REQUEST_ID = ContextVar('request_id')
REQUEST_ID.set(uuid.uuid1())

# new handler
class DictHandler(logging.Handler): # Inherit from logging.Handler
        def __init__(self, log_dict):
                logging.Handler.__init__(self)
                self.log_dict = log_dict
        def emit(self, record):
                self.log_dict[str(REQUEST_ID.get())].append(record.msg)

def get_child_logger(root_name, child_name):
    return logging.getLogger(root_name).getChild(child_name)


if __name__ == "__main__":
    # load config file
    logging.config.fileConfig("logging.conf")


    root_logger = logging.root
    parent_logger = logging.getLogger('declaration')
    log_dict = defaultdict(list)
    dict_handler = DictHandler(log_dict)
    dict_handler.setFormatter(logging.root.handlers[0].formatter)
    dict_handler.setLevel(logging.WARN)
    parent_logger.addHandler(dict_handler)
    parent_logger = myLogger(parent_logger, {'request_id': ''}) # adapter
    REQUEST_ID.set(uuid.uuid1())

    parent_logger.debug("debug_parent")
    parent_logger.info("info_root")
    parent_logger.warning("warn_root")
    parent_logger.error("error_root")
    REQUEST_ID.set(uuid.uuid1())

    child_logger = get_child_logger('declaration', 'blahblah_module')
    child_logger.debug("debug_module")
    child_logger.info("info_module")
    child_logger.warning("warn_module")
    child_logger.error("error_module")

    print(log_dict)
