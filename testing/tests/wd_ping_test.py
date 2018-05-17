import testing_base as base
import testing_logger as logger
from pymodbus.pdu import ExceptionResponse

@base.testClass('wpt')
class Ping_Test(base.testingBase):
    '''
This test simply pings the target over modbus, according
to the command parameters.
Uses: -i, -s, -p, -w, -l, -f, -t
'''

    def __init__(self, cfg):
        self.log = logger.get_logger('Ping_Test')
        self.log.info("Look at the modbus watchdog to check for false triggers")
        self.config = cfg
        self.ping = 0
        base.testingBase.__init__(self, cfg)

    def init_test(self):
        self.log.info("setup target state")
        self.log.info("sleep time between iterations: %.3f"%(self.config.sleep))
        self.log.info("iterations between pings: %d"%(self.config.ping))

    def iterate_test(self):
        # read bulk data
        regs = self.client.client.read_holding_registers(0, 10)
        if ExceptionResponse is type(regs):
            self.log.error("read configurations from target failed: %s"%(str(regs)))
