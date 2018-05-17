import time
import testing_base as base
import testing_logger as logger

@base.testClass('ctr')
class CT_Testing(base.testingBase):
    '''
This test is used to activate a heater so that the current 
can be measured.
Uses: -i, -z, -v, -s, -p, -l, -f
'''
    def __init__(self, cfg):
        self.log = logger.get_logger("CT_Testing")
        self.log.info("testing the actual Current Transformer readings")
        #self.config = cfg
        base.testingBase.__init__(self, cfg)

    def init_test(self):
        self.log.debug("force open loop to %f %% output"%(self.config.value))
        self.log.info("setup target state")
        self.client.write_zone(30000, self.config.zone, 0x03, arg_type='uint16')
        self.client.write_zone(30003, self.config.zone, self.config.value, arg_type='float')

    def iterate_test(self):
        val = self.client.read_input_zone(20000, self.config.zone, arg_type='float')
        self.log.info("raw temperature: %f"%(val))
        val = self.client.read_input_zone(30003, self.config.zone, arg_type='float')
        self.log.info("percent readback value: %f"%(val))
        val = self.client.read_input_zone(30005, self.config.zone, arg_type='float')
        self.log.info("ct current reading: %f"%(val))
