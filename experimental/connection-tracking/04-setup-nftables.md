# nftables

nftables does the hard work of logging all the connections being made

## Configuration
```
sudo echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/50-ipforward.conf
sudo service procps force-reload
sudo sysctl -w net.ipv4.ip_forward=1
```

Add to `/etc/nftables.conf`:
```
#!/usr/sbin/nft -f

flush ruleset

table ip nat {
  chain postrouting {
    type nat hook postrouting priority 0; log

    # Masquerade outgoing traffic
    oifname enp0s3 masquerade;
  }
}
```

# Restart the service

```
sudo service nftables restart
```
