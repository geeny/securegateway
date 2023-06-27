# ulogd

## Installation

```
sudo apt install ulogd2 ulogd2-json
```

## Configuration

Configure the following in `/etc/ulogd.conf`:

```
[global]

logfile="syslog"

loglevel=3

plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_filter_HWHDR.so"
plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_filter_IFINDEX.so"
plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_filter_IP2STR.so"
plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_inppkt_NFLOG.so"
plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_raw2packet_BASE.so"
plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_output_JSON.so"

stack=log1:NFLOG,base1:BASE,ifi1:IFINDEX,ip2str1:IP2STR,mac2str1:HWHDR,json1:JSON

[log1]
group=1

[json1]
sync=1
file="/var/log/ulog/ulogd.json"
timestamp=1
device="sg"
eventv1=1
```

## Restart the service

```
sudo service ulogd2 restart
```

## Sample ulogd JSON data

Sample data can be found in `files/ulogd-sample-data.json`
