import argparse
import re
import sys
import testing_base as base

# does not use the logger because this happens before the logger exists
class testingConfig:

    def __init__(self):
        args = self.command_line()
        for item in vars(args):
            self.add_item(args, item)

    def add_item(self, nspc, name):
        val = getattr(nspc, name)
        if str is type(val):
            exec("self.%s = '%s'"%(name, val))
        elif int is type(val):
            exec("self.%s = %d"%(name, val))
        elif float is type(val):
            exec("self.%s = %f"%(name, val))
        elif bool is type(val):
            pass # don't save bools
        else:
            raise Exception("Unknown type encountered in Config: %s"%(type(val)))

    def command_line(self):
        parser = argparse.ArgumentParser(description="General purpose testing system", add_help=False, epilog='')
        parser.add_argument('-h', 
                            dest='help', 
                            #type=bool,
                            default=False, 
                            action='store_true',
                            help='show help messages (False)')

        parser.add_argument('-V', 
                            dest='verbose', 
                            #type=bool,
                            default=False, 
                            action='store_true',
                            help='print test classes documentation (False)')

        parser.add_argument('-i', 
                            dest='ip_addr', 
                            type=str,
                            default='192.168.0.1', 
                            help='ip address (192.168.0.1)')

        parser.add_argument('-z', 
                            dest='zone', 
                            type=int,
                            default='0', 
                            help='zone number (0-7)')

        parser.add_argument('-v', 
                            dest='value', 
                            type=float,
                            default='10.0', 
                            help='percent power to set the output (10.0)')

        parser.add_argument('-s', 
                            dest='sleep', 
                            type=float,
                            default='1.0', 
                            help='sleep interval between test iterations (1.0)')

        parser.add_argument('-p', 
                            dest='ping', 
                            type=int,
                            default='60', 
                            help='number of iterations between ping messages (60)')

        parser.add_argument('-w', 
                            dest='watchdog', 
                            type=int,
                            default='2000', 
                            help='milliseconds for watchdog to kick (2000)')

        parser.add_argument('-l', 
                            dest='logs', 
                            type=str,
                            default='i', 
                            help='set the logging level "i"nfo, "e"rror, "d"ebug (i)')

        parser.add_argument('-f', 
                            dest='filename', 
                            type=str,
                            default='logfile.txt', 
                            help='Name of the file to place logging into. (logfile.txt)')

        parser.add_argument('-m', 
                            dest='max_temp', 
                            type=float,
                            default=100.0, 
                            help='Maximum temerature allowed on a plate. (100.0)')

        test_list = []
        for item in base.TEST_NAMES:
            test_list.append(item)
            
        parser.add_argument('-t', 
                            dest='test', 
                            type=str,
                            default='', 
                            help='required test name (%s)'%('|'.join(test_list)))
                            #required=True)

        args = parser.parse_args()
        epilog = ''
        if args.help:
            if args.verbose:
                # build the epilog
                for item in base.TEST_NAMES:
                    epilog += "\n%s: %s%s"%(item, base.TEST_NAMES[item].__name__, base.TEST_NAMES[item].__doc__)
            else:
                epilog += "\nFor more help use '%s -h -V'\n"%(sys.argv[0])

            parser.print_help()
            print epilog
            parser.exit(0)
        else:
            epilog = "\nERROR: For more help use '%s -h -V'\n"%(sys.argv[0])
            if args.test == '':
                print epilog
                print "\nRequired value for '-t' parameter (%s)"%('|'.join(test_list))
                parser.exit(1)

            if args.zone < 0 or args.zone > 7:
                print epilog
                print "\nInvalid zone. Valid values are 0 - 7"
                parser.exit(1)
            
            if args.value < 0 or args.value > 100.0:
                print epilog
                print "\nInvalid value. Valid values are 0.0 - 100.0"
                parser.exit(1)

            m = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', args.ip_addr)
            if None == m:
                print epilog
                print "\nInvalid ip address. Valid values are of the form xxx.xxx.xxx.xxx, where x is a decimal digit."
                parser.exit(1)

        return args

