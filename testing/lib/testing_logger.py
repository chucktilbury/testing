import logging

def setup_logger(cfg): #**kwargs):

    fname = cfg.filename

    fmt = '%(asctime)s - %(name)-12s - %(levelname)-5s - %(message)s'
    dfmt = '%a, %d %b %Y %H:%M:%S'
    # file log level is always "debug"
    logging.basicConfig(level=logging.NOTSET, 
                        format=fmt,
                        datefmt=dfmt,
                        filename=fname,
                        filemode='w')
    console = logging.StreamHandler()

    if cfg.logs.upper()[0] == 'C':
        console.setLevel(logging.CRITICAL)
    elif cfg.logs.upper()[0] == 'E':
        console.setLevel(logging.ERROR)
    elif cfg.logs.upper()[0] == 'W':
        console.setLevel(logging.WARNING)
    elif cfg.logs.upper()[0] == 'I':
        console.setLevel(logging.INFO)
    elif cfg.logs.upper()[0] == 'D':
        console.setLevel(logging.DEBUG)
    elif cfg.logs.upper()[0] == 'N':
        console.setLevel(logging.NOTSET)
    else:
        console.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt, datefmt=dfmt)
    console.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(console)

    return logger

def get_logger(name):
    return logging.getLogger(name)