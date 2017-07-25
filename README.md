# Collect Lustre Stats through Telegraf

The main point of developing this Python script is to be able to summarize multiple Lustre stats described in a configuration file  
and report them in a format compatible with the **InfluxDB** timeseries database.

Although this script can be executed directly on the command line for testing purposes, it is meant to be executed periodically by  
the **Telegraf** monitoring agent.

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

Only the export statistics on the OSSs:
~~~
[LustreStats]
lustre_metric_types = obdfilter.*.exports.*@*.stats
~~~

Stats can be added or removed as needed. Two examples of configuration files can be found under the *stats_config* subdir.

## Lustre Statistics

The statistics are broken down by *OST* for every OSS.

Descriptions about the Lustre statistics can be found at the following web page:  
http://wiki.lustre.org/Lustre_Monitoring_and_Statistics_Guide

## InfluxDB timeseries format

The following are examples of the output generated by the script after reading the Lustre stats.  
*Note*: the output is formatted in order to be compatible with the InfluxDB timeseries DB.  
Reference: (https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/)

In general:
~~~
<measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]
~~~

The script format the Lustre statistics in three different timeseries:
- RW_stats
- ops_stats
- lustre_stats

Lustre *read/write statistics*
~~~
RW_stats,ost_name=OST_name read_bytes_samples=113022841,read_bytes_min=4096,read_bytes_max=1048576,read_bytes_sum=22335639511040 1500984347000000000
RW_stats,ost_name=OST_name write_bytes_samples=26818323,write_bytes_min=1,write_bytes_max=1048576,write_bytes_sum=5062687832653 1500984347000000000
~~~

The numbers reported by the previous lines has to be interpreted as follows:

- (read|write)_bytes = number of times (samples) the OST has handled a read or write.
- (read|write)_bytes_min = the minimum read/write size.
- (read|write)_bytes_max = maximum read/write size.
- (read|write)_bytes_sum = sum of all the read/write requests in bytes, the quantity of data read/written.

Lustre *OSS stats per export*

In this case *RW_stats* will reports also the IP of the Lustre client accessing the OSS.

~~~
RW_stats,ost_name=OST_name,client_ip=192.168.1.2 read_bytes_samples=92468,read_bytes_min=4096,read_bytes_max=262144,read_bytes_sum=19600334848 1500984747000000000
RW_stats,ost_name=OST_name,client_ip=192.168.1.2 write_bytes_samples=45918,write_bytes_min=1,write_bytes_max=262144,write_bytes_sum=9975502527 1500984747000000000
ops_stats,ost_name=OST_name,op_type=get_info op_requests=175457 1500984747000000000
ops_stats,ost_name=OST_name,op_type=disconnect op_requests=15 1500984747000000000
ops_stats,ost_name=OST_name,op_type=setattr op_requests=3056 1500984747000000000
ops_stats,ost_name=OST_name,op_type=punch op_requests=831 1500984747000000000
ops_stats,ost_name=OST_name,op_type=sync op_requests=7934 1500984747000000000
ops_stats,ost_name=OST_name,op_type=preprw op_requests=138386 1500984747000000000
ops_stats,ost_name=OST_name,op_type=commitrw op_requests=138386 1500984747000000000
ops_stats,ost_name=OST_name,op_type=quotactl op_requests=12 1500984747000000000
ops_stats,ost_name=OST_name,op_type=ping op_requests=105804 1500984747000000000
[...]
RW_stats,ost_name=OST_name,client_ip=192.168.1.3 read_bytes_samples=2,read_bytes_min=4096,read_bytes_max=4096,read_bytes_sum=8192 1500984747000000000
RW_stats,ost_name=OST_name,client_ip=192.168.1.3 write_bytes_samples=262,write_bytes_min=16,write_bytes_max=262144,write_bytes_sum=36580864 1500984747000000000
ops_stats,ost_name=OST_name,op_type=get_info op_requests=66 1500984747000000000
ops_stats,ost_name=OST_name,op_type=disconnect op_requests=1772 1500984747000000000
ops_stats,ost_name=OST_name,op_type=punch op_requests=263 1500984747000000000
ops_stats,ost_name=OST_name,op_type=sync op_requests=5 1500984747000000000
ops_stats,ost_name=OST_name,op_type=preprw op_requests=264 1500984747000000000
ops_stats,ost_name=OST_name,op_type=commitrw op_requests=264 1500984747000000000
ops_stats,ost_name=OST_name,op_type=ping op_requests=165529 1500984747000000000
~~~

Lustre *operation statistics*
~~~
ops_stats,ost_name=OST_name,op_type=get_info op_requests=5037158 1500984347000000000
ops_stats,ost_name=OST_name,op_type=set_info_async op_requests=2 1500984347000000000
ops_stats,ost_name=OST_name,op_type=connect op_requests=26733 1500984347000000000
ops_stats,ost_name=OST_name,op_type=reconnect op_requests=2547 1500984347000000000
ops_stats,ost_name=OST_name,op_type=disconnect op_requests=26299 1500984347000000000
ops_stats,ost_name=OST_name,op_type=statfs op_requests=62365651 1500984347000000000
ops_stats,ost_name=OST_name,op_type=create op_requests=8795 1500984347000000000
ops_stats,ost_name=OST_name,op_type=destroy op_requests=360629 1500984347000000000
ops_stats,ost_name=OST_name,op_type=setattr op_requests=140788 1500984347000000000
ops_stats,ost_name=OST_name,op_type=punch op_requests=316291 1500984347000000000
ops_stats,ost_name=OST_name,op_type=sync op_requests=1785069 1500984347000000000
ops_stats,ost_name=OST_name,op_type=preprw op_requests=139841164 1500984347000000000
ops_stats,ost_name=OST_name,op_type=commitrw op_requests=139841164 1500984347000000000
ops_stats,ost_name=OST_name,op_type=quotactl op_requests=832095 1500984347000000000
ops_stats,ost_name=OST_name,op_type=ping op_requests=90155646 1500984347000000000
[...]
~~~

Lustre statistics about *available and total disk space*
~~~
lustre_stats,ost_name=OST_name kbytesfree=12575394176 1495111943000000000
lustre_stats,ost_name=OST_name kbytestotal=22772060416 1495111943000000000
~~~

Lustre statistics about *available and total inodes*
~~~
lustre_stats,ost_name=OST_name filesfree=120365628 1495111943000000000
lustre_stats,ost_name=OST_name filestotal=120751442 1495111943000000000
~~~

Lustre statistics about *locks*
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

## Running the script with Telegraf

In order to send the metrics to InfluxDB the script has to be executed through the *Telegraf* monitoring agent.  
Take a look into the simple *telegraf.conf* file included in the repo (under the telegraf_config subdir) for a  
ready to use configuration file.

The script will be called by Telegraf using the *inputs.exec* plugin.

## Running the script interactively on the command line
~~~
get-stats.py -f oss_stats
~~~

The output will be printed directly on stdout but it can be also redirected to an output file or piped to another command.
