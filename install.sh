#!/bin/bash
echo "Install System Requriements"
sudo apt-get install python-dev libatlas-base-dev

echo "Install Pythons Deps"
python3 -m pip install -r requirements.txt

echo "Setting up env"
cp -n .env.example .env
nano ./.env 
set -e

echo "Setting up Tide Service"
service_location="/lib/systemd/system/tide.service"
if [ -f "$service_location" ]; then
    echo "$service_location exists. Skipping Creation"
else 
    cat <<EOF > $service_location
Description=Tidetracker eInk
After=multi-user.target
[Service]
Type=simple
Restart=always
RestartSec=10
WorkingDirectory=$PWD
User=$USER
ExecStart=/usr/bin/python3 -m tidetracker.run
[Install]
WantedBy=multi-user.target
EOF
fi


sudo chmod 644 $service_location

echo "Reloading and Starting Daemons"
sudo systemctl daemon-reload
sudo systemctl enable tide.service
sudo systemctl start tide.service
sudo systemctl status tide.service
echo ""
echo "Setup Complete"
echo ""
echo "To start/stop/etc.. "
echo "> sudo systemctl start|stop|restart|status tide"
echo ""
echo "To view logs you can use:"
echo "> sudo journalctl -u tide"
echo ""
echo "The config for the service lives here $service_location"
echo ""
echo "Happy Hacking =)"



