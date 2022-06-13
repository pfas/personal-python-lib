from distutils import dep_util
import logging.config

DEBUG = True

# log file handler
log_fh_dict = dict()


LOG_FMT = '%(asctime)s [%(processName)s] [%(threadName)s] [%(name)s] [%(levelname)s] [%(filename)s: line %(lineno)d]: %(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'

def logfile_handler(log_filepath):  #  thread unsafe
    global log_fh_dict
    if log_filepath not in log_fh_dict:
        formatter = logging.Formatter(LOG_FMT, DATE_FMT)
        fh = logging.FileHandler(log_filepath)
        fh.setLevel(logging.INFO)

        fh.setFormatter(formatter)
        log_fh_dict[log_filepath] = fh
    
    return log_fh_dict[log_filepath] 


def logger_factory(log_name, log_filepath, debug:True):
    global DEBUG
    DEBUG = debug
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    fh = logfile_handler(log_filepath)
    logger.addHandler(fh)
    
    if DEBUG:
        for h in logger.handlers:
            h.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(LOG_FMT, DATE_FMT)
        sh.setFormatter(formatter)

        logger.addHandler(sh)

    return logger

