import sys, os
# Add the tests and library to the path for execution
p = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(p, 'lib'))
sys.path.append(os.path.join(p, 'tests'))

# import the actual application
import testing_logger as logger
import testing_base as base
import testing_config as config

# import the actual tests. importing the tests adds them to the test list
# see the command line help for more information
import ct_read_test
import wd_read_test
import wd_ping_test
import wd_timer_test
import multi_interval_test
import interval_test


# Don't allow this to be "import"ed
if __name__ == '__main__':
    # intentionally don't trap exceptions here
    # check the python version and abort if it's not 2.7
    if sys.version_info < (2,7) or sys.version_info > (3,):
        raise Exception("This program requires python version 2.7")

    cfg = config.testingConfig()
    logger.setup_logger(cfg)
    log = logger.get_logger("main proc")
    base.testingRun(cfg)
