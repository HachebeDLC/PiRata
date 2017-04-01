sudo apt-get install apt-transport-https -y --force-yes;  
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key  | sudo apt-key add -  ;
echo "deb https://dev2day.de/pms/ jessie main" | sudo tee /etc/apt/sources.list.d/pms.list  ;
sudo apt-get update  ;
sudo apt-get install -t jessie plexmediaserver deluged deluge-console deluge-web apache2 -y  ;
echo pi:Hochobo:10 >> ~/.config/deluge/auth

sudo cp -R  PiRata/apache2 /etc/apache2
sudo cp -R www/ /var/
sudo a2enmod proxy proxy_html proxy_http headers
sudo service apache2 restart
sudo git clone http://github.com/RuudBurger/CouchPotatoServer.git
