sudo apt-get install apt-transport-https -y --force-yes;  
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key  | sudo apt-key add -  ;
echo "deb https://dev2day.de/pms/ jessie main" | sudo tee /etc/apt/sources.list.d/pms.list  ;
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FDA5DFFC
echo "deb http://apt.sonarr.tv/ master main" | sudo tee /etc/apt/sources.list.d/sonarr.list
sudo apt-get update  ;
sudo apt-get install -t jessie plexmediaserver deluged deluge-console deluge-web nginx -y  ;
echo pi:Hochobo:10 >> ~/.config/deluge/auth
sudo git clone http://github.com/RuudBurger/CouchPotatoServer.git
sudo cp CouchPotatoServer/init/ubuntu /etc/init.d/couchpotato
sudo nano /etc/init.d/couchpotato
sudo chmod +x /etc/init.d/couchpotato
sudo update-rc.d couchpotato defaults
sudo apt-get update
sudo apt-get install nzbdrone 
sudo cp deluged.service /etc/systemd/system/deluged.service
