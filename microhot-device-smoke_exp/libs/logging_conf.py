import logging
import logging.config

def singleton(cls):
    def get_singleton():
        singleton_cls = {}
        if cls not in singleton_cls:
            singleton_cls[cls] = cls()
        return singleton_cls[cls]
    return get_singleton()


@singleton
class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.handler = logging.StreamHandler()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '%(asctime)s %(levelname)-8s %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)



