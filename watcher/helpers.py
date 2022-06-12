import logging

def prepare_logger(path_to_log):
    log = logging.getLogger()  
    for hdlr in log.handlers[:]:  
        log.removeHandler(hdlr)

    fileh = logging.handlers.RotatingFileHandler(path_to_log, maxBytes=10000, backupCount=5)

    formatter = logging.Formatter('%(asctime)s [%(name)s:%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s')
    fileh.setFormatter(formatter)
    
    log.addHandler(fileh)
    log.setLevel(logging.DEBUG)