import os
import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    fmt = '%(name)s - %(asctime)s - %(pathname)s [line:%(lineno)d] - %(levelname)s: %(message)s'

    def __init__(self, level='info', when='midnight', back_count=5):
        # 如果日志文件夹不存在，则创建
        log_dir = "logs"  # 日志存放文件夹名称
        log_path = os.getcwd() + os.sep + log_dir
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        self.logger = logging.getLogger('root')
        format_str = logging.Formatter(self.fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # print(log_path + os.sep + 'access.log')
        # th = handlers.TimedRotatingFileHandler(filename='./' + log_dir + os.sep + "access.log", when=when, backupCount=back_count, encoding='utf-8')
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        # th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        # self.logger.addHandler(th)

    def get_logger(self):
        logger = self.logger
        return logger


if __name__ == '__main__':
    log = Logger(level='debug')
    logger = log.get_logger()
    logger.debug('debug')
    logger.info('info')
    # log.logger.warning('警告')
    # log.logger.error('报错')
    # log.logger.critical('严重')
    # Logger(level='error').logger.error('error')
