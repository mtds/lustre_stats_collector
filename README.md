# Lustre Stats gathering

This Python script is able to summarize the Lustre stats described in a configuration file.

## Config files examples

Example for OSSs:
~~~
[LustreStats]
lustre_metric_types = obdfilter.*OST*.kbytesfree,obdfilter.*OST*.kbytestotal,obdfilter.*OST*.filesfree,obdfilter.*OST*.filestotal,obdfilter.*.stats,ldlm.namespaces.filter-*.pool.granted
~~~

Example for MDSs:
~~~
[LustreStats]
lustre_metric_types = osd-*.*.kbytesfree,osd-*.*.kbytestotal,osd-*.*.filesfree,osd-*.*.filestotal,mdt.*MDT*.md_stats,mdt.*MDT*.num_exports
~~~

Stats can be added or removed as needed.

## Lustre Statistics

The statistics are broken down by *OST* for every OSS.  
Reference: http://wiki.lustre.org/Lustre_Monitoring_and_Statistics_Guide

The following are examples of the output generated by the script after the Lustre stats.  
*Note*: the output is formatted in order to be compatible with the InfluxDB timeseries DB.  
(https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/)

Lustre *read/write statistics*:
~~~
RW_stats,ost_name=OST_name read_bytes=503962017,read_bytes_min=4096,read_bytes_max=1048576,read_bytes_sum=119135327100928 1495110922000000000
RW_stats,ost_name=OST_name write_bytes=34357916,write_bytes_min=1,write_bytes_max=1048576,write_bytes_sum=6171357502687 1495110922000000000
~~~

The numbers reported by the previous lines has to be interpreted as follows:

- (read|write)_bytes = number of times (samples) the OST has handled a read or write.
- (read|write)_bytes_min = the minimum read/write size.
- (read|write)_bytes_max = maximum read/write size.
- (read|write)_bytes_sum = sum of all the read/write requests in bytes, the quantity of data read/written.

Lustre *operation statistics*:
~~~
ops_stats,ost_name=OST_name get_info=8325872 1495111943000000000
ops_stats,ost_name=OST_name set_info_async=1 1495111943000000000
ops_stats,ost_name=OST_name connect=8535 1495111943000000000
ops_stats,ost_name=OST_name reconnect=871 1495111943000000000
ops_stats,ost_name=OST_name disconnect=8537 1495111943000000000
[...]
~~~

Lustre statistics about *available and total disk space*:
~~~
lustre_stats,ost_name=OST_name kbytesfree=12575394176 1495111943000000000
lustre_stats,ost_name=OST_name kbytestotal=22772060416 1495111943000000000
~~~

Lustre statistics about *available and total inodes*:
~~~
lustre_stats,ost_name=OST_name filesfree=120365628 1495111943000000000
lustre_stats,ost_name=OST_name filestotal=120751442 1495111943000000000
~~~

Lustre statistics about *locks*:
- lock count
- lustre distributed lock manager (ldlm) granted locks
- ldlm lock grant rate
- ldlm lock cancel rate
~~~
lustre_stats,ost_name=OST_name granted=24888 1495111943000000000
lustre_stats,ost_name=OST_name lock_count=24888 1495111943000000000
lustre_stats,ost_name=OST_name cancel_rate=0 1495111943000000000
lustre_stats,ost_name=OST_name grant_rate=2 1495111943000000000
~~~

## Running the script

Interactively on the command line:
~~~
get-stats.py -f oss_stats
~~~

Telegraf/InfluxDB:  
In order to send the metrics to InfluxDB the script has to be executed through the *Telegraf* monitoring agent.  
Take a look into the simple telegraf.conf file included in the repo for a ready to use configuration file.

