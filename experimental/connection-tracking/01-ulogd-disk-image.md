### ulogd disk image

We create this disk image to prevent our machine from running out of
disk splace due to ulogd logs. (Which also prevents from a DDoS attack
on the machine.)

```
dd if=/dev/zero of=/var/log/ulog.disk bs=1G count=1
chown root.adm /var/log/ulog.disk
chmod 750 /var/log/ulog.disk
mkfs.ext4 /var/log/ulog.disk


mkdir /var/log/ulog
chown root.adm /var/log/ulog
chmod 750 /var/log/ulog

mount -t ext4 /var/log/ulog.disk /var/log/ulog
```
