auto lo
iface lo inet loopback
iface eth0 inet dhcp

# iface wlan0 inet manual
# wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
auto wlan0
iface wlan0 inet static
address 10.188.26.11
netmask 255.255.255.0
gateway 10.188.26.11
