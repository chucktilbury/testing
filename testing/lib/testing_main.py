import testing_base as base
import testing_config as config
import testing_logger as logger
import logging

if __name__ == '__main__':

    try:
        logger.setup_logger(name='asdf', level='debug', fname='somefile.txt')
        log = logging.getLogger("main")
        conf = config.testingConfig()
        
        log.info('test program starts')
        base.testingRun(conf)
        log.info('test program ends')
    except Exception as e:
        #logger.error(e)
        log.exception(e)


