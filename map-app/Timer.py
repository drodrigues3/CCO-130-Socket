import time
import logging

FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
LOG_FILENAME = './tile-cache/app.log'
logging.basicConfig(format=FORMAT, filename=LOG_FILENAME, level=logging.DEBUG)
logger = logging.getLogger('map-app')

class Timer:
    def __init__(self, function_name=None):
        self.function_name = function_name

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        logger.info(str(self.interval) + 's spent on ' + self.function_name + '().')
