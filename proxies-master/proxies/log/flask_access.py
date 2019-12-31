import os
import time
from logging import handlers
from logging.handlers import TimedRotatingFileHandler

from loguru import logger

"""自定义日志处理类"""


class MyLoggingHandler(TimedRotatingFileHandler):

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        TimedRotatingFileHandler.__init__(self, filename, when=when, interval=interval, backupCount=backupCount,
                                          encoding=encoding, delay=delay, utc=utc, atTime=atTime)

    def computeRollover(self, currentTime):
        # 将时间取整
        t_str = time.strftime(self.suffix, time.localtime(currentTime))
        t = time.mktime(time.strptime(t_str, self.suffix))
        return TimedRotatingFileHandler.computeRollover(self, t)

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        # 修改内容--开始
        # 在多进程下，若发现dfn已经存在，则表示已经有其他进程将日志文件按时间切割了，只需重新打开新的日志文件，写入当前日志；
        # 若dfn不存在，则将当前日志文件重命名，并打开新的日志文件
        if not os.path.exists(dfn):
            try:
                self.rotate(self.baseFilename, dfn)
            except FileNotFoundError:
                # 这里会出异常：未找到日志文件，原因是其他进程对该日志文件重命名了，忽略即可，当前日志不会丢失
                pass
        # 修改内容--结束
        # 原内容如下：
        """
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        """

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class Logging:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance
        else:
            cls._instance = object.__new__(cls)
            return cls._instance

    def __init__(self):
        self.file = None

    def get_logger(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(BASE_DIR, 'logs')
        if not os.path.exists(path):
            os.mkdir(path)
        logger.remove()
        th = MyLoggingHandler(filename=os.path.join(path, f"xl_access_pid-{2019}.log"),
                                               when="midnight", backupCount=20,
                                               encoding='utf-8')
        logger.add(th)
        logger.info(f'*****************logger in pid:{os.getpid()} ********************')
        return logger


if __name__ == '__main__':
    # th = MyLoggingHandler(
    #     filename='/home/uniccc/xl-project/xl-spider/xl_project/fengxianjiankong/fengxianjiankong/logs/access.log',
    #     when='S')
    log = Logging()
    logger = log.get_logger()
    # logger.add(th)
    logger.info('aaaaaaaaaaaaa')
