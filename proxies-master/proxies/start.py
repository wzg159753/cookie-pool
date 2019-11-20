from run import Run
from util.configtion import logger


if __name__ == '__main__':
    logger.info('开始运行')
    start = Run()
    start.run()