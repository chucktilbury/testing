import time
import testing_base as base
import testing_logger as logger

@base.testClass('ctm')
class CT_Multi_Interval_Test(base.testingBase):
    '''
This test measures the interval between CT readings when all
of the channels are active.
Uses: -i, -s, -p, -f, -t
'''
    def __init__(self, cfg):
        self.log = logger.get_logger('CT_Multi_Interval_Test')
        self.log.info("Testing the interval that the current transformer is polled")
        self.config = cfg
        self.old_temp = [0.0]*8
        self.old_time = [time.time()]*8
        self.new_temp = [0.0]*8
        base.testingBase.__init__(self, cfg)

    def init_test(self):
        self.log.debug("force open loop to %f %% output"%(self.config.value))
        self.log.info("setup target state")

        self.client.write_coil(8, True)
        self.client.write_coil(1, True)
        self.client.write_coil(2, True)
        self.client.write_coil(0, True)

        for idx in range(8):
            self.client.write_zone(30000, idx, 0x03, arg_type='uint16')
            self.client.write_zone(30003, idx, self.config.value, arg_type='float')
            
    def iterate_test(self):
        for idx in range(8):
            self.new_temp[idx] = self.client.read_input_zone(30005, idx, arg_type='float')

            if self.new_temp[idx] != self.old_temp[idx]:
                self.old_temp[idx] = self.new_temp[idx]
                t = time.time() - self.old_time[idx]
                self.log.info("Zone %d elapsed time: %02d:%02d:%02d (%0.3f)"% (idx+1, t // 3600, (t % 3600 // 60), (t % 60 // 1), self.new_temp[idx]))
                self.old_time[idx] = time.time()

    def check_maxtemp(self, zone):
        val = self.client.read_input_zone(20000, self.config.zone, arg_type='float')
        if val > self.config.max_temp:
            self.log.error("Maximum temperature exceeded: %f (%f)"%(val, self.config.max_temp))
            #self.client.reset()
            raise Exception("Maximum temperature exceeded: %f (%f)"%(val, self.config.max_temp))

    def ping_action(self):
        v = self.client.decode_holding_args(65101, {'arg_type':'uint16'})
        if v != 0:
            self.log.error("looks like the modbus watchdog has kicked!")
            self.log.info("reset watchdog trigger")
            self.client.write(65101, 0, arg_type='uint16')

        for idx in range(8):
            self.client.write_zone(30000, idx, 0x03, arg_type='uint16')
            self.check_maxtemp(idx)
