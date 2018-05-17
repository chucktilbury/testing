from pymodbus.client.sync import ModbusTcpClient as MClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.compat import iteritems
from pymodbus.pdu import ExceptionResponse

import testing_logger as logger

class modbusClient:

    def __init__(self, args):
        self.logger = logger.get_logger('modbusClient')
        self.logger.debug("init modbus client")
        self.client = MClient(args.ip_addr)
        self.args = args
        if False is self.client.connect():
            raise Exception("cannot connect to ip address: %s"%(args.ip_addr))

        # list of arg types and their size, by words, not bytes
        self.args_list = {'float':{'size':2},        
                            'uint64':{'size':4},
                            'int64':{'size':4},
                            'uint32':{'size':2},
                            'int32':{'size':2},
                            'uint16':{'size':1},
                            'int16':{'size':1},
                            'int8':{'size':1},
                            'uint8':{'size':1},
                            'string':{'size':0}}

    def close(self):
        self.client.close()

    def reset(self):
        '''reset the target'''
        self.logger.info("resetting the target")
        self.write(60000, 0x4655, arg_type='uint16')

    def read_coil(self, reg):
        #print reg
        self.logger.debug("read coil (%d)"%(reg))
        #retv = self.client.read_coils(reg, 1)
        retv = self.client.read_coils(0, 9)
        if ExceptionResponse is type(retv):
            raise Exception("read_coil transaction failed with function code: %d: %s"%(retv.exception_code, str(retv)))
        else:
            #print retv.bits
            return retv.bits[reg]

    def write_coil(self, reg, val):
        self.logger.debug("write coil (%d, %r)"%(reg, val))
        retv = self.client.write_coil(reg, val)
        if ExceptionResponse is type(retv):
            raise Exception("write_coil transaction failed with function code: %d: %s"%(retv.exception_code, str(retv)))

    def read_holding(self, reg, **kwargs):
        self.logger.debug("read holding raw (%d, %s)"%(reg, str(kwargs)))
        return self.decode_holding_args(reg, kwargs)

    def read_holding_zone(self, reg, zone, **kwargs):
        reg = reg + (zone * 100)
        self.logger.debug("read holding zone (%d)"%(reg))
        return self.decode_holding_args(reg, kwargs)

    def read_input(self, reg, **kwargs):
        self.logger.debug("read input raw (%d)"%(reg))
        return self.decode_input_args(reg, kwargs)

    def read_input_zone(self, reg, zone, **kwargs):
        reg = reg + (zone * 100)
        self.logger.debug("read input zone (%d)"%(reg))
        return self.decode_input_args(reg, kwargs)

    def write(self, reg, val, **kwargs):
        self.logger.debug("write raw (%d, %d)"%(reg, val))
        arg = self.build_args(val, kwargs)
        result = self.client.write_registers(reg, arg, skip_encode=True, unit=1)
        if ExceptionResponse is type(result):
            raise Exception("write_raw transaction failed with function code: %d: %s"%(result.exception_code, str(result)))

    def write_zone(self, reg, zone, val, **kwargs):
        reg = reg + (zone * 100)
        self.logger.debug("write zone (%d, %d)"%(reg, val))
        arg = self.build_args(val, kwargs)
        result = self.client.write_registers(reg, arg, skip_encode=True, unit=1)
        if ExceptionResponse is type(result):
            raise Exception("write_zone transaction failed with function code: %d: %s"%(result.exception_code, str(result)))

    def arg_size(self, kwargs):
        if kwargs['arg_type'] == 'string':
            if not 'strlen' in kwargs:
                raise Exception("string value requires length in kwargs")
            siz = kwargs['strlen']
        elif kwargs['arg_type'] in self.args_list:
            siz = self.args_list[kwargs['arg_type']]['size']
        else:
            # should never happen
            raise Exception("unknown parameter type string given: %s"%(kwargs['arg_type']))

        return siz
        

    def decode_input_args(self, reg, kwargs):

        rval = self.client.read_input_registers(reg, self.arg_size(kwargs))
        if ExceptionResponse is type(rval):
            raise Exception("read input reg transaction failed with function code: %d: %s"%(rval.exception_code, str(rval)))

        decoder = BinaryPayloadDecoder.fromRegisters(rval.registers, byteorder=Endian.Big)
        if 'arg_type' in kwargs:
            if kwargs['arg_type'] == 'float':    val = decoder.decode_32bit_float()
            elif kwargs['arg_type'] == 'uint64': val = decoder.decode_64bit_uint()
            elif kwargs['arg_type'] == 'int64':  val = decoder.decode_64bit_int()
            elif kwargs['arg_type'] == 'uint32': val = decoder.decode_32bit_uint()
            elif kwargs['arg_type'] == 'int32':  val = decoder.decode_32bit_int()
            elif kwargs['arg_type'] == 'uint16': val = decoder.decode_16bit_uint()
            elif kwargs['arg_type'] == 'int16':  val = decoder.decode_16bit_int()
            elif kwargs['arg_type'] == 'int8':   val = decoder.decode_8bit_int()
            elif kwargs['arg_type'] == 'uint8':  val = decoder.decode_8bit_uint()
            elif kwargs['arg_type'] == 'string': val = decoder.decode_string()
            else: raise Exception("unknown parameter type given: %s"%(kwargs['arg_type']))
        else:
            val = decoder.decode_16bit_uint()
        
        return val

    def decode_holding_args(self, reg, kwargs):

        rval = self.client.read_holding_registers(reg, self.arg_size(kwargs))
        if ExceptionResponse is type(rval):
            raise Exception("read holding reg transaction failed with function code: %d: %s"%(rval.exception_code, str(rval)))

        decoder = BinaryPayloadDecoder.fromRegisters(rval.registers, byteorder=Endian.Big)
        if 'arg_type' in kwargs:
            if kwargs['arg_type'] == 'float':    val = decoder.decode_32bit_float()
            elif kwargs['arg_type'] == 'uint64': val = decoder.decode_64bit_uint()
            elif kwargs['arg_type'] == 'int64':  val = decoder.decode_64bit_int()
            elif kwargs['arg_type'] == 'uint32': val = decoder.decode_32bit_uint()
            elif kwargs['arg_type'] == 'int32':  val = decoder.decode_32bit_int()
            elif kwargs['arg_type'] == 'uint16': val = decoder.decode_16bit_uint()
            elif kwargs['arg_type'] == 'int16':  val = decoder.decode_16bit_int()
            elif kwargs['arg_type'] == 'int8':   val = decoder.decode_8bit_int()
            elif kwargs['arg_type'] == 'uint8':  val = decoder.decode_8bit_uint()
            elif kwargs['arg_type'] == 'string': val = decoder.decode_string()
            else: raise Exception("unknown parameter type given: %s"%(kwargs['arg_type']))
        else:
            val = decoder.decode_16bit_uint()
        
        return val

    def build_args(self, arg, kwargs):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big) #, wordorder=Endian.Big)
        if 'arg_type' in kwargs:
            if kwargs['arg_type'] == 'float':    builder.add_32bit_float(arg)
            elif kwargs['arg_type'] == 'uint64': builder.add_64bit_uint(arg)
            elif kwargs['arg_type'] == 'int64':  builder.add_64bit_int(arg)
            elif kwargs['arg_type'] == 'uint32': builder.add_32bit_uint(arg)
            elif kwargs['arg_type'] == 'int32':  builder.add_32bit_int(arg)
            elif kwargs['arg_type'] == 'uint16': builder.add_16bit_uint(arg)
            elif kwargs['arg_type'] == 'int16':  builder.add_16bit_int(arg)
            elif kwargs['arg_type'] == 'int8':   builder.add_8bit_int(arg)
            elif kwargs['arg_type'] == 'uint8':  builder.add_8bit_uint(arg)
            elif kwargs['arg_type'] == 'string': builder.add_string(arg)
            else: raise Exception("unknown parameter type given: %s"%(kwargs['arg_type']))
        else:
            builder.add_16bit_uint(arg)

        val = builder.build()
        return val

