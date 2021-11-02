import uuid
import logging

request_id = uuid.uuid1()

## 새로운 속성 생성 -> 기존 record 속성처럼 사용가능
extra = {'request_id':request_id}

logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(request_id)s : %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)

logger = logging.LoggerAdapter(logger, extra)
logger.info('Heyyy')