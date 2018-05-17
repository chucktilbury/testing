
import time
import testing_modbus_client as client
import testing_logger as logger

TEST_NAMES = {}

# decorator for the tests adds the test name and class to the global list
def testClass(fname):
    log = logger.get_logger("testClassDecorator")
    def rebuild(cls):
        log.debug("class name is %s"%(cls.__name__))
        log.debug("friendly name is %s"%(fname))
        TEST_NAMES[fname] = cls # save the class in the list

        class Wrapper:
            def __init__(self, *args, **kwargs):
                self.wrapped = cls(*args, **kwargs)

            def __getattr__(self, name):
                log.debug('Getting the {} of {}'.format(name, self.wrapped))
                return getattr(self.wrapped, name)

            # demonstration purposes
            #def added(self):
            #    print 'made it here'
            #    return 'blart'

        return Wrapper
    return rebuild

# select a test and run it
class testingRun:

    def __init__(self, cfg):
        self.log = logger.get_logger("testingRun")
        self.log.debug("init testing runner")
        self.cfg = cfg
        tests = TEST_NAMES

        if self.cfg.test in tests:
            self.log.info("Running test: \"%s\" from \"%s\""%(self.cfg.test, tests[self.cfg.test].__name__))
            t = tests[self.cfg.test](self.cfg)
            t.run()
        else:
            raise Exception("unknown test specified: %s"%(self.cfg.test))

class testingBase:

    # These methods are inteded to be overridden
    def init_test(self):
        raise Exception("tests must implement the init_test method")

    def iterate_test(self):
        raise Exception("tests must implement the iterate_test method")

    # default action is to reset the device
    def uninit_test(self):
        self.client.reset()

    # default action is to do nothing
    def ping_action(self):
        pass

    # These methods are intended to not be overridden
    # call this init from the child test class in order to create the modbus object
    def __init__(self, cfg, name='test'):
        self.log = logger.get_logger('testingBase.'+name)
        self.log.debug("test base init")
        self.config = cfg
        self.client = client.modbusClient(self.config)
        self.ping = 0

    def run(self):
        self.log.info("test starts")
        try:
            self.log.info("-"*20+" press CTRL-C to end test "+"-"*20)
            # perform actions related to the test initialization here
            self.init_test()

            self.log.info("test iterations starting")
            while True:
                self.iterate_test()

                if self.ping > self.config.ping: # If sleep is 1S and ping is 60, then print ever minute
                    self.ping = 0
                    self.log.info("test alive")
                    self.ping_action()
                else:
                    self.ping += 1

                time.sleep(self.config.sleep)
        
        except KeyboardInterrupt as e:
            # This is the only exit point unless the test is killed externally
            self.log.info("-"*30+" BREAK "+"-"*30)
            self.uninit_test()

        except Exception as e:
            self.log.error("test error")
            self.uninit_test()
            raise

        self.log.info("test ends normally")
    