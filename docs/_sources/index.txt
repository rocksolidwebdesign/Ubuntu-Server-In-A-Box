.. Ubuntu Server In A Box documentation master file, created by
   sphinx-quickstart on Fri Mar 11 01:00:47 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ubuntu Server In A Box Fabfile
==============================

.. _about:

What Is It?
===========

A  python script  to  automatically install  a complete  web
server  using  Ubuntu  10.10  including

* Web Server
* Database Server
* Git Repository Server
* EMail Server

Suitable for  development or  staging servers that  may host
multiple  domains. Possibly  even  useful  for a  production
server.

.. _quick-start:

Quick Start
===========

To give it the old college try, use this handy installer script::

    bash < <( curl http://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install )

This script should  install Fabric if you don't  have it and
should initiate a session, all  you need is the hostname and
root password of an Ubuntu 10.10 server.

Ideally this would be a new Rackspace Cloud Server instance.

.. _requirements:

Requirements
============

You need:

* Python http://python.org/
* Fabric (the package for Python) http://fabfile.org/
* An Ubuntu 10.10 system
* Root shell access

These fab tasks are specifically intended to be used with an
Ubuntu 10.10 system that has  shell access to a literal root
account -  namely Rackspace  Cloud Server  instances running
Ubuntu 10.10  Business Edition,  previously known  as Ubuntu
Server 10.10.

Other setups are planned for future releases.

.. _basics:

Basic Usage
===========

Download from github::

    git clone http://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box.git
    cd Ubuntu-Server-In-A-Box

Install requirements (Fabric is currently the only requirement)::

    pip install -r requirements.txt

Copy the example settings file as ``settings.py``::

    cd quickfab/ubuntu
    cp settings.py.sample settings.py

Customize the settings to your taste, full documentation can be found in :doc:`settings`::

    vim settings.py

Run the main fab task::

    fab setup_all

Run the clean task to delete your locally cached config files::

    fab clean

There are far more tasks than just these two and in fact I would encourage you
to use single tasks at a time because that will help you get an understanding
of what the system actually does and how to customize it for your needs

You can get a complete list of all the fab tasks with::

    fab --list

Full documentation for tasks can be found in :doc:`tasks`

.. _install:

Complete Install Instructions
=============================

Here are the longer  and more complete download instructions
with explanations::

    user@somehost ~/fabfiles/ubuntucloud$ git clone http://github.com/rocksolidwebdesign/QuickFab.git cloudfab
    user@somehost ~$ cd cloudfab

you'll need Python's Fabric best retrieved through pip::

    user@somehost ~/cloudfab$ sudo pip install -r requirements.txt

if you don't have pip, or a pip version that's recent enough to
support requirements, then you probably have ``easy_install``::

    user@somehost ~/cloudfab$ sudo easy_install -r requirements.txt

and if you  don't have ``easy_install`` or  pip, then you'll
probably  need and  want  to  get one  or  the other  before
continuing.::

    user@somehost ~/cloudfab$ sudo apt-get install python-pip

otherwise, if you're not on ubuntu for your local machine,
please see the Fabric documentation for installation:

http://docs.fabfile.org/en/1.0.0/installation.html

next edit  settings.py you'll  need to  at least  change the
server's hostname and master  usernames including the deploy
user and  the main  username. you'll  probably also  want to
change the name and email  for the git repository admin. and
you may wish to specify a different webroot for example.

there is  further simple configuration  that can be  done in
terms of defining your team members, but this example should
work and  install out of the  box with the example  users if
you're just testing this for the  first time, so you can get
a feel for how it works::

    user@somehost ~/cloudfab$ fab setup_all

.. _overview:

What It Does
============

This  project  aims to  install  a  fully working  and  semi
production ready web  server using Ubuntu 10.10  and for use
somewhere along your deployment chain, most likely as dev or
staging, but possibly  this could be a base for  prod if you
add some better security measures and whatnot.

To use this  fabfile you will need any  Ubuntu 10.10 server,
available over  the internet  or local network  with literal
root access, no sudo for now, though that is planned.

.. _results:

What You Get
============

When you are done you will have a server with the following
general setup in terms of users and software

* Apache with  some default  vhosts and  a few  other simple
  vhosts  for  acting  as  proxy to  the  Django  and  Rails
  development servers
* Nginx with  some default  example vhosts  and a  few other
  simple vhosts for acting as  a reverse proxy to Apache and
  as proxy to the Django and Rails development servers
* One deploy  user account that  can edit all  website files
  and who can restart the webserver without a password. this
  user may or may not also have full sudo privileges
* One  master   user  account  with  full   sudo  privileges
  essentially a root equivalent
* A number of  web developers who also have  shell access to
  the  server and  who will  also want  shell account  these
  users will  also have  similarly limited  privileges, even
  further  limited in  their  abilities to  muck about  with
  other people's files

.. _package-versions:

Specifically What You Get
=========================

A basic LAMP setup

* Apache HTTPD 2.2.x
* PHP 5.3.x
* MySQL 5.1.x

An email server setup

* Postfix SMTP
* Dovecot SASL
* Dovecot IMAP/POP3

A repository server

* git
* gitolite
* subversion
* subversion webdav

Other web server related goodies

* Nginx 0.9.x
* Python 2.6 and ``virtualenv``
* Ruby 1.8.x and ``rvm``
* PostgreSQL 8.4
* SQLite 3

.. _virtual-machine:

Using a Virtual Machine
=======================

If  you are  just  setting  up a  dev  server  on a  virtual
machine,  then most  likely you've  installed Ubuntu  Server
10.10 and  it didn't come  with a  root password but  only a
regular user account with sudo  and that's not yet supported
by this fabfile

The good  news, however, is  that adding a password  to your
root account is actually fairly easy, something like::

    user@somehost ~$ sudo su -
    root@somehost ~# passwd YOURROOTPASSWORDHERE

and then you'll be able to actually log in as the root user.
this  should work  well if  you're using  this on  a virtual
machine for development.

.. _documentation-index:

Full Documentation
==================

.. toctree::
    :maxdepth: 2

    settings
    config_dir
    tasks

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
