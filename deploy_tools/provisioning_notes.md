
Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv
* mysqlclient


eg, on Ubuntu

        sudo apt-get install nginx git python3 python3-pip
        sudo apt-get install virtualenv

        ## MySQL on python 2
        sudo apt-get install mysql-server libmysqlclient-dev python-dev 
        pip install mysql-python

        ## MySQL on python 3
        sudo apt-get install libmysqlclient-dev python-dev
        pip install mysqlclient

## Nginx Virtual Host config

* see nginx.template.con
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/usename

	/home/username
	|__sites
	   |__SITENAME
	      |__database
	      |__source
	      |__stativ
	      |__virtualenv
