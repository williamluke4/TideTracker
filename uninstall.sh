echo "Stopping Services.."
sudo systemctl stop tide
sudo systemctl disable tide
echo "Deleting..."
sudo rm -rf /lib/systemd/system/tide.service
