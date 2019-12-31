import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect
import sys
import servicemanager

from run import Run

from multiprocessing import Process


class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Cookie-Pool"
    _svc_display_name_ = "Python Cookie Service"
    _svc_description_ = "python service code "

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True

    def _getLogger(self):
        logger = logging.getLogger('[PythonService]')

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        import time
        self.logger.info("service is run....")
        while self.run:
            run = Test()
            run.run()
        # run = Run()
        # run.run()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


class Test():

    def __init__(self):
        self.logger = self._getLogger()

    def run_tester(self):
        while True:
            print(123)

    def _getLogger(self):
        logger = logging.getLogger('[PythonService]')

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def run(self):
        self.logger.info('启动')
        # self.run_tester()
        tester_process = Process(target=self.run_tester)
        tester_process.start()


if __name__ == '__main__':
    # win32serviceutil.HandleCommandLine(PythonService)
    start = Run()
    start.run()
