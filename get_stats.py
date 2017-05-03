#!/usr/bin/env python

#
# Extract the stats from /proc/fs/lustre and print them on the cmd line.
#

#
# NOTE: the output format is meant to be compatible with the InfluxDB line protocol.
#       (ref: https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/)
#

#
# Lustre statistics: http://wiki.lustre.org/Lustre_Monitoring_and_Statistics_Guide
#

import ConfigParser
import getopt
import re
import subprocess
import sys
import time

def get_stats(lustre_stats):

   # Call 'lctl get_param' and get the result (subprocess() return always a string):
   metric = subprocess.check_output(['lctl', 'get_param', lustre_stats])

   # Temporary host the OST name:
   ost_name = ''

   #
   # If 'metric' contains 'snapshot_time' it means we are dealing with multiline values:
   #
   if 'snapshot_time' in metric:
      for item in metric.splitlines()[1::]:
          if 'obdfilter' in item:
             ost_name = item.split('.')[1]
          elif 'snapshot_time' in item:
             stats_t = (filter(None, metric.splitlines()))[1]
             timestamp = re.findall(r'\d+', stats_t)[0]
             timestamp = int(timestamp) * 1000000000 # force a conversion in nanoseconds ('snapshot_time' is in seconds.usecs)
          else: 
             if '_bytes' not in item:
                stats_type, stats_requests, unit_str, reqs_str = filter(None, item.split(" "))
                print "%s Stats %s=%s %d" % (ost_name,stats_type,stats_requests,timestamp)
             else:
                read_write_ops, events, samples_str, unit_str, min_rd_wr, max_rd_wr, sum_rd_wr = filter(None, item.split(" "))
                print "%s Read_Write_Events %s=%s,%s_min=%s,%s_max=%s,%s_sum=%s %d" % (ost_name,read_write_ops,events,read_write_ops,min_rd_wr,read_write_ops,max_rd_wr,read_write_ops,sum_rd_wr,timestamp)
   else:
      timestamp = int(time.time()) * 1000000000 # extract the integer part of time() and convert it in nanoseconds
      value_list = metric.splitlines()
      for item in value_list:
          measurement, value = item.split("=")
          print "Lustre %s=%s %d" % (measurement,value,timestamp)

def main(argv):

   # Config filename string:
   config_file = ''

   # The script will accept only two options:
   # -h print (generic help msg)
   # -f config_file (a config file in INI format)

   try:
       opts, args = getopt.getopt(argv,"hf::")
   except getopt.GetoptError:
       print 'get_stats.py -f <cfgfile>'
       sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'get_stats.py -f <cfgfile>'
         sys.exit()
      elif opt in ("-f"):
         config_file = arg
         # Read the stats to check from the configuration file:
         config = ConfigParser.RawConfigParser()
         config.read(config_file)

         # Cycle through the stats list:
         for item in config.get('LustreStats','lustre_metric_types').split(','):
            get_stats(item)

if __name__ == "__main__":
   main(sys.argv[1:])
