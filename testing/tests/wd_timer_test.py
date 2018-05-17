import time
import testing_base as base
import testing_logger as logger
from pymodbus.pdu import ExceptionResponse

@base.testClass('wdtt')
class WD_Timer_Testing(base.testingBase):
    '''
This test does a basic modbus watchdog timer test
by reading many registers periodically. If the 
watchdog trips then that is a problem.
Uses: -i, -s, -p, -w, -l, -f, -t
'''
    def __init__(self, cfg):
        self.log = logger.get_logger("WD_Timer_Testing")
        self.log.info("Look at the modbus watchdog to check for false triggers")
        self.config = cfg

        self.total_resets = 0
        self.last_reset = 0.0
        base.testingBase.__init__(self, cfg, "WD_Timer_Testing")

    def init_test(self):
        # just reset the wd counter
        self.client.write(65101, 0, arg_type='uint16')

    def iterate_test(self):
        # read the watchdog timeout counter and if it's not zero, then 
        # increment the total and reset it.
        value = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
        if value != 0:
            self.total_resets += value
            self.last_reset = time.time()
            self.log.error("*"*40)
            self.log.error("modbus watchdog triggered %d times"%(self.total_resets))
            self.log.debug("reset watchdog trigger")
            self.client.write(65101, 0, arg_type='uint16')

        # read bulk data and remember how much time it took
        regs = self.client.client.read_holding_registers(0, 100)
        if ExceptionResponse is type(regs):
            self.log.error("read from target failed: %s"%(str(regs)))
            raise Exception("failed to read from the target")


    def ping_action(self):
        # print how many reset there have been and when the last one was
        self.log.info("there have been %d watchdog resets"%(self.total_resets))
        if self.last_reset != 0.0:
            t = time.time() - self.last_reset
            self.log.info("last reset was %02d:%02d:%02d (%0.3fS) ago"%(t // 3600, (t % 3600 // 60), (t % 60 // 1), t))
