import uuid
import logging
from contextvars import ContextVar
from collections import defaultdict

# custom loggerAdapter
class myLogger(logging.LoggerAdapter):
    def process(self,msg,kwargs):
        return '%s : %s' % (var.get(),msg)  ,kwargs

simple_formatter = logging.Formatter("[%(name)s %(asctime)s] %(message)s")
var = ContextVar('request_id')
var.set(uuid.uuid1())

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
syslog_handler = logging.StreamHandler()
syslog_handler.setFormatter(simple_formatter)
logger.addHandler(syslog_handler)

# new handler
class DictHandler(logging.Handler): # Inherit from logging.Handler
        def __init__(self, log_dict):
                logging.Handler.__init__(self)
                self.log_dict = log_dict
        def emit(self, record):     
                self.log_dict[str(var.get())].append(record.msg)

log_dict = defaultdict(list)
list_handler = DictHandler(log_dict)
list_handler.setLevel(logging.WARN)
logger.addHandler(list_handler)


logger = myLogger(logger, {'request_id': ''})

logger.debug('heyyy_debug')
var.set(uuid.uuid1())
logger.info('heyyy_info')
var.set(uuid.uuid1())
logger.warning('heyyy_warn')
var.set(uuid.uuid1())
logger.error('heyyy_error')


print(log_dict) # for test