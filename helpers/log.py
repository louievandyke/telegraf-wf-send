import logging
import logging.handlers



class Log(object):

    def __init__(self, logname):
        self.logname = logname


    def logger(self):
        logger = logging.getLogger(self.logname)
        logger.setLevel(level=logging.INFO)
        fh = logging.handlers.RotatingFileHandler('logs/%s.log' %(self.logname),
                                                  maxBytes=1024000,
                                                  backupCount=5)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)
        return logger