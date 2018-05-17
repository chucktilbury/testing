$ python testing/testing.py -hV
usage: testing.py [-h] [-V] [-i IP_ADDR] [-z ZONE] [-v VALUE] [-s SLEEP]
                  [-p PING] [-w WATCHDOG] [-l LOGS] [-f FILENAME]
                  [-m MAX_TEMP] [-t TEST]

General purpose testing system

optional arguments:
  -h           show help messages (False)
  -V           print test classes documentation (False)
  -i IP_ADDR   ip address (192.168.0.1)
  -z ZONE      zone number (0-7)
  -v VALUE     percent power to set the output (10.0)
  -s SLEEP     sleep interval between test iterations (1.0)
  -p PING      number of iterations between ping messages (60)
  -w WATCHDOG  milliseconds for watchdog to kick (2000)
  -l LOGS      set the logging level "i"nfo, "e"rror, "d"ebug (i)
  -f FILENAME  Name of the file to place logging into. (logfile.txt)
  -m MAX_TEMP  Maximum temerature allowed on a plate. (100.0)
  -t TEST      required test name (wdrt|ctr|wpt|wdtt|ctm|cti)

wdrt: WDT_Testing
This test does a basic modbus watchdog timer test
by reading some registers periodically. If the
watchdog trips then that is a problem.
Uses: -i, -s, -p, -w, -l, -f, -t

ctr: CT_Testing
This test is used to activate a heater so that the current
can be measured.
Uses: -i, -z, -v, -s, -p, -l, -f

wpt: Ping_Test
This test simply pings the target over modbus, according
to the command parameters.
Uses: -i, -s, -p, -w, -l, -f, -t

wdtt: WD_Timer_Testing
This test does a basic modbus watchdog timer test
by reading many registers periodically. If the
watchdog trips then that is a problem.
Uses: -i, -s, -p, -w, -l, -f, -t

ctm: CT_Multi_Interval_Test
This test measures the interval between CT readings when all
of the channels are active.
Uses: -i, -s, -p, -f, -t

cti: CT_Interval_Test
This test measures the interval between CT readings with
one specific channel activated.
Uses: -i, -z, -v, -s, -p, -l, -f, -t

