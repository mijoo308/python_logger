import logging

''' logger adapter와 유사하지만 다른 방식'''
old_factory = logging.getLogRecordFactory()

def createRecordFactory(context_id):
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.custom_attribute = context_id
        return record
    return record_factory


logging.basicConfig(format="%(custom_attribute)s - %(message)s")
logging.setLogRecordFactory(createRecordFactory("whatever"))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")

logging.setLogRecordFactory(createRecordFactory("whatever2"))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")