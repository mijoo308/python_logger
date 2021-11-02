import logging


''' Formatter '''
simple_formatter = logging.Formatter("[%(name)s] %(message)s")
complex_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
)

''' Handler '''
# Handler 1 : stream 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(simple_formatter) # 포매터 설정
console_handler.setLevel(logging.DEBUG)        # level 설정


# Handler 2: file 핸들러
file_handler = logging.FileHandler("error.log")
file_handler.setFormatter(complex_formatter)
file_handler.setLevel(logging.ERROR)

''' Logger '''
# 루트 로거
root_logger = logging.getLogger() # 이름을 입력하지 않으면 루트 로거
root_logger.addHandler(console_handler) # 핸들러 1 설정
root_logger.addHandler(file_handler)    # 핸들러 2 설정
root_logger.setLevel(logging.INFO)   # log level 설정
                                     # root는 info 이상만

# 부모 로거
parent_logger = logging.getLogger("declaration") # 이름을 입력하면 루트로거의 하위 로거가 됨
# parent_logger.setLevel(logging.INFO) # 따로 log level을 설정하지 않으면 상위 log level과 같음

# 자식 로거
child_logger = logging.getLogger("declaration.drive") # .으로 자식 로거 설정
child_logger.setLevel(logging.DEBUG) #child는 debug 이상만

# 전파하고 싶지 않을 때
# child_logger.propagate = False


if __name__ == "__main__":
    root_logger.debug("디버그")
    root_logger.info("정보")
    root_logger.error("오류")

    parent_logger.debug("디버그")
    parent_logger.info("정보")
    parent_logger.error("오류")

    child_logger.debug("디버그")
    child_logger.info("정보")
    child_logger.error("오류")