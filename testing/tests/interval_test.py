import time
import testing_base as base
import testing_logger as logger

@base.testClass('cti')
class CT_Interval_Test(base.testingBase):
    '''
This test measures the interval between CT readings with
one specific channel activated.
Uses: -i, -z, -v, -s, -p, -l, -f, -t
'''
    def __init__(self, cfg):
        self.log = logger.get_logger('CT_Interval_Test')
        self.log.info("Testing the interval that the current transformer is polled")
        self.config = cfg
        self.old_temp = 0.0
        self.old_time = time.time()
        base.testingBase.__init__(self, cfg)

    def init_test(self):
        self.log.debug("force open loop to %f %% output"%(self.config.value))
        self.log.info("setup target state")
        # set the configuration to "manual"
        self.client.write_zone(30000, self.config.zone, 0x03, arg_type='uint16')
        # set the output percent setting to the command parameter
        self.client.write_zone(30003, self.config.zone, self.config.value, arg_type='float')

        self.client.write_coil(8, True)
        self.client.write_coil(1, True)
        self.client.write_coil(2, True)
        self.client.write_coil(0, True)

    def check_maxtemp(self, zone):
        val = self.client.read_input_zone(20000, self.config.zone, arg_type='float')
        if val > self.config.max_temp:
            self.log.error("Maximum temperature exceeded: %f (%f)"%(val, self.config.max_temp))
            #self.client.reset()
            raise Exception("Maximum temperature exceeded: %f (%f)"%(val, self.config.max_temp))

    def iterate_test(self):
        self.new_temp = self.client.read_input_zone(30005, self.config.zone, arg_type='float')
                    
        if self.new_temp != self.old_temp:
            self.old_temp = self.new_temp
            t = time.time() - self.old_time
            self.log.info("Elapsed time between readings: %02d:%02d:%02d (%0.3f)"% (t // 3600, (t % 3600 // 60), (t % 60 // 1), self.new_temp))
            #logger.info("Elapsed time between readings (raw): %f"%(t))
            self.old_time = time.time()

    def ping_action(self):
        v = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
        if v != 0:
            self.log.error("looks like the modbus watchdog has kicked!")
            self.log.info("reset watchdog trigger")
            self.client.write(65101, 0, arg_type='uint16')

        self.client.write_zone(30000, self.config.zone, 0x03, arg_type='uint16')
        self.check_maxtemp(self.config.zone)

