import uuid
import logging
from contextvars import ContextVar
var = ContextVar('request_id')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
syslog = logging.StreamHandler()
logger.addHandler(syslog)


class myLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '%s : %s' % (var.get(), msg), kwargs


logger = myLogger(logger, {'request_id': ''})


for i in range(3):
    var.set(uuid.uuid1())
    logger.info('heyyy')