disactive (){
  sudo cp wifi/interfaces.back /etc/network/interfaces
  sudo cp wifi/dnsmasq.back /etc/dnsmasq.conf
  sudo systemctl disable hostapd
  sudo systemctl disable dnsmasq
}

active (){
  sudo cp wifi/interfaces.mod /etc/network/interfaces
  sudo cp wifi/dnsmasq.mod /etc/dnsmasq.conf
  sudo systemctl enable hostapd
  sudo systemctl enable dnsmasq
}

if [[ $1 == "start" ]]
then
  echo "Activating WiFi Hotspot"
  active
else
  echo "Disactivating WiFi Hotspot"
  disactive
fi
sudo reboot
