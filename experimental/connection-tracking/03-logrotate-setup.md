# logrotate

logrotate helps with file sizes

# Configuration

Inside `/etc/logrotate-ulogd-json.conf`:

```
su root adm
dateext
dateformat -%s

/var/log/ulog/*.json {
  rotate -1
  missingok
  size 1
  nocompress
  create 640 ulog adm

  sharedscripts
  postrotate
    if [ -d /run/systemd/system ] && command systemctl >/dev/null 2>&1 && systemctl is-active --quiet ulogd2.service; then
      systemctl kill --kill-who main --signal=SIGHUP ulogd2.service
    fi
  endscript
}
```

Inside `/etc/cron.d/logrotate-ulogd-json`:

```
* * * * * root /usr/sbin/logrotate -f /etc/logrotate-ulogd-json.conf
```

## Restart crond

```
sudo service cron reload
```
