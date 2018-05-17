import time
import testing_base as base
import testing_logger as logger
from pymodbus.pdu import ExceptionResponse

@base.testClass('wdrt')
class WDT_Testing(base.testingBase):
    '''
This test does a basic modbus watchdog timer test
by reading some registers periodically. If the 
watchdog trips then that is a problem.
Uses: -i, -s, -p, -w, -l, -f, -t
'''
    def __init__(self, cfg):
        self.log = logger.get_logger("WDT_Testing")
        self.log.info("Look at the modbus watchdog to check for false triggers")
        self.config = cfg
        self.data_size = 120
        self.old_value = 0
        self.ping = 0
        self.old_wd = 0
        self.test_elapse = 0.0
        self.sleep_elapse = 0.0
        self.av_test = 0.0
        self.av_sleep = 0.0
        self.total_wd_resets = 0
        base.testingBase.__init__(self, cfg)

    def init_test(self):
        self.log.info("setup target state")
        self.log.info("data size: %d"%(self.data_size))
        self.log.info("sleep time between iterations: %.3f"%(self.config.sleep))
        self.log.info("iterations between pings: %d"%(self.config.ping))
        
        # set up the watchdog timeout
        value = self.client.decode_holding_args(65100, {'arg_type':'uint16'})
        self.old_wd = value
        self.log.info("existing watchdog timeout is set to %d"%(value))
        if value != self.config.watchdog:
            self.log.info("resetting watchdog timeout to %d"%(self.config.watchdog))
            self.client.write(65100, self.config.watchdog, arg_type='uint16')
            value = self.client.decode_holding_args(65100, {'arg_type':'uint16'})
            if value == self.config.watchdog:
                self.log.info("watchdog set okay")
            else:
                self.log.error("watchdog set FAILED")
                sys.exit("Fatal Error")

        # set up the even count
        value = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
        self.log.info("watchdog trigger is %d"%(value))
        if value != 0:
            self.log.info("reset watchdog trigger")
            self.client.write(65101, 0, arg_type='uint16')
            value = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
            self.log.info("watchdog trigger is now %d"%(value))
            if value == 0:
                self.log.info("reset watchdog trigger okay")
            else:
                self.log.error("reset watchdog trigger FAILED")
                sys.exit("Fatal Error")

    def iterate_test(self):
        # read bulk data
        regs = self.client.client.read_holding_registers(10000, 10)
        if ExceptionResponse is type(regs):
            self.log.error("read configurations from target failed: %s"%(str(regs)))

        # read the watchdog timeout counter
        value = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
        if value != 0:
            self.old_value += 1
            self.total_wd_resets += 1
            self.log.error("*"*80)
            self.log.error("modbus watchdog triggered %d times"%(self.old_value))
            self.log.debug("reset watchdog trigger")
            self.client.write(65101, 0, arg_type='uint16')
            value = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
            self.log.debug("watchdog trigger is now %d"%(value))
            if value != 0:
                self.log.error("failed to reset watchdog trigger")
                sys.exit("Fatal Error")

    def run(self):
        self.log.info("test starts")
        try:
            self.log.info("--------------------- press CTRL-C to end test ------------------------")
            # perform actions related to the test initialization here
            self.init_test()

            self.log.info("test iteratins starting")
            while True:
                # perform the actions associated with the test iteration here
                tt = time.time()
                t = time.time()
                self.iterate_test()
                self.test_elapse = time.time() - t
                # check to see if the test took longer than the watchdog
                # note that elapsed time is in seconds and the watchdog time is in milliseconds
                if self.config.watchdog < int(self.test_elapse * 1000.0):
                    self.log.error("-"*80)
                    self.log.error("test took longer than the watchdog: %.3f seconds"%(self.test_elapse))

                # running average
                self.av_test = (self.av_test + self.test_elapse) / 2

                t = time.time()
                time.sleep(self.config.sleep)
                self.sleep_elapse = time.time() - t
                if self.config.watchdog < int(self.sleep_elapse * 1000.0):
                    self.log.error("-"*80)
                    self.log.error("test took longer than the watchdog: %.3f seconds"%(self.sleep_elapse))

                # running average
                self.av_sleep = (self.av_sleep + self.sleep_elapse) / 2

                if self.ping > self.config.ping: # If sleep is 1S and ping is 60, then print ever minute
                    self.ping = 0
                    self.log.info("test alive: average test: %.3f average loop: %.3f"%(self.av_test, self.av_sleep + self.av_test))
                else:
                    self.ping += 1

                tt = time.time() - tt
                if self.config.watchdog < int(tt * 100):
                    self.log.error("-"*80)
                    self.log.error("test loop took longer than the watchdog: %.3f seconds"%(tt))

        
        except KeyboardInterrupt as e:
            # This is the only exit point unless the test is killed externally
            self.log.info("------------------------------ BREAK ---------------------------------")
            # clean up at the end of the test run.
            self.uninit_test()

        except Exception as e:
            self.log.error("test error")
            raise

        self.log.info("total number of watchdog resets: %d"%(self.total_wd_resets))
        self.log.info("test ends normally")
