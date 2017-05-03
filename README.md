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

Stats can be added or removed as needed. The list of interesting Lustre statistics for MDT and OSS was taken from: http://wiki.lustre.org/Lustre_Monitoring_and_Statistics_Guide

## Running the script

~~~
get-stats.py -f oss_stats
~~~

*Note*:the output format of the script is formatted to be compatible with the InfluxDB timeseris DB.  
(https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/)

In order to interact with InfluxDB the script has to be executed through the *Telegraf* monitoring agent.

