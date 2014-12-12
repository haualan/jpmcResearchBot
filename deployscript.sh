
sudo pip intall -U numpy

# need both to install all packages, must use 2nd line to download standard language parsers to a central location
sudo pip intall -U nltk
sudo python -m nltk.downloader -d /usr/share/nltk_data all


# MySQL-python requires instance of mysql as depenedancy, not required for usage
sudo apt-get install mysql
sudo apt-get install libmysqlclient-dev

sudo pip install MySQL-python
sudo nano /etc/apache2/sites-available/jpmcResearchBot.conf

<VirtualHost *:80>
    ServerName mywebsite.com
    ServerAdmin admin@mywebsite.com
    WSGIScriptAlias / /var/www/jpmcResearchBot/flaskapp.wsgi
    <Directory /var/www/jpmcResearchBot/jpmcResearchBot/>
      Order allow,deny
      Allow from all
    </Directory>
    Alias /static /var/www/jpmcResearchBot/jpmcResearchBot/static
    <Directory /var/www/jpmcResearchBot/jpmcResearchBot/static/>
      Order allow,deny
      Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


cd /var/www/jpmcResearchBot
sudo nano flaskapp.wsgi

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/jpmcResearchBot/")

from jpmcResearchBot import app as application
application.secret_key = 'secret-key'