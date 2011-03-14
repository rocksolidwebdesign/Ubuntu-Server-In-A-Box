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

    bash < <( curl https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install )
    fab setup

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

Customize the settings to your  taste (or don't, you can run
the script as is and it  will prompt you for your hostname),
full documentation can be found in :doc:`settings`::

    vim settings.py

Run the main fab task::

    fab setup

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
* One deploy user account that pretty much owns everything.s
  The deploy  user can  edit all website  file and  who cans
  restart the webserver without a password. this user may ors
  may not also have full sudo privilege                    s
* One  master   user  account  with  full   sudo  privileges
  essentially a root equivalent
* A number of  web developers who also have  shell access to
  the  server and  who will  also want  shell account  these
  users will  also have  similarly limited  privileges, even
  further  limited in  their  abilities to  muck about  with
  other people's files

Where's My Stuff?
=================

-------------------
Your Web Site Files
-------------------
Well, by  default your stuff goes  into ``/var/www`` because
that's  a pretty  standard place,  you can  however use  the
``webroot_dir``  setting  to  change this  to  your  liking,
perhaps to ``/myserver`` or something.

This webroot directory is not really the webroot per say but
more like  the server root  which houses the many  web roots
for your various CGI, PHP, Ruby and Python apps.

The Canonical Layout
--------------------
There are three main folders corresponding to the thre basic
different types  of apps, PHP  (and Perl and CGI),  Ruby and
Python::

    /var/www/apache
    /var/www/rails
    /var/www/django

And  the idea  is  that  each project  is  a self  contained
"website" or  "virtual host",  and that  each project  has a
folder  for the  code and  then a  subfolder for  the public
files, by  default it's  called ``public`` oddly  enough, so
that your public  users will never be able to  stumble in to
your source code.

PHP Projects
------------
Another way  of putting  this is  that the  canonical layout
here goes like this::

    /var/www/<SERVER_TYPE>/<PROJECT_NAME>/public

So  for   example  if   we  had  a   PHP  web   site  called
wonderwidget.com, then the actual PHP files would live in::

    /var/www/apache/wonderwidget.com

And you'd  put all your  images and stylesheets,  e.g. JPEGs
and CSS files in::

    /var/www/apache/wonderwidget.com/public

-------------
Ruby Versions
-------------

This  setup  installs the  standard  ruby  1.8 package  that
ships  with  Ubuntu  but  it installs  the  latest  rubygems
from rubygems.org,  which provides ``/usr/bin/gem1.8`` and  so I
manually symlink that to ``/usr/bin/gem``  to make life a little
nicer, so  you should  be able  to sudo  gem install  foo to
install gems to the system 1.8 ruby.

By default the system ruby comes with the rails 2.3.8 gem to
stay compatible with radiant.

The latest  ruby 1.9.2 be found  in RVM for the  deploy user
along with the latest 3.0 rails. Simply ssh in as the deploy
user and then run::

    rvm 1.9.2
    which rails

and that should hopefully satisfy your curiosities. You can
of course, continue to use rvm as normal to install gemsets
and other rubies like ``ree`` or what have you.

You can  then start a  new rails project by  doing something
like this,  and this should  work for both the  system rails
and the RVM rails::

    cd /var/www/rails
    rails new wonderwidget
    cd wonderwidget
    script/server

Both the  system and rvm  install use passenger.  The system
install actually uses the  passenger gem and custom compiles
and installs it using ``passenger-install-apache2-module``

Passenger  is of  course,  as usual,  still  available as  a
standalone binary as ``passenger`` e.g. ::

    passenger start -a 127.0.0.1 -p 3000 -d

Which brings me to

Rails Projects
--------------

Rails  and  Django projects  don't  follow  the strict  FQDN
naming scheme that the PHP  sites do. This is because having
those names on  the Apache based sites makes  it much easier
to reverse proxy those sites with nginx.

For example if we had  a rails web site called rainmaker.com
then your actual rails project root would be::

    /var/www/rails/rainmaker

And would have contents like::

    /var/www/rails/rainmaker/app/
    /var/www/rails/rainmaker/config/
    /var/www/rails/rainmaker/Gemfile
    /var/www/rails/rainmaker/Rakefile

And you'd put all your images and stylesheets, e.g. JPEGs and CSS files in::

    /var/www/rails/rainmaker.com/public

-------------------
Python Environments
-------------------

Ubuntu depends on a minimal python install so python 2.6 is
already available and that's what we make use of here, we're
also leveraging the Ubuntu mod_wsgi package for Apache, though
there's actually a mod_uwsgi package available that's probably
more recent and up to date be.

The pip that comes with ubuntu is fairly heavily out of date
and instead of mucking about with attempting an upgrade, we
just download and install the (hopefully) latest version directly
from pypi. Pip requires distribute so this is done for distribute
as well.

Virtualenv along with virtualenvwrapper are then installed
via pip and the deploy user is given basic virtualenv capabilities
to run e.g. ``mkvirtualenv`` and ``workon``

Most of the basic necessities for a Django CMS app including
Django, MySQL and imaging packages are installed via pip
into the main system. These same packages can be installed
to a default test environment for Django called ``djangocms_test``

To use this environment simply ssh as the ``deploy`` user
and run::

    workon djangocms_test

And then you can use ``django-admin.py`` to create yourself
a Django app and you'll have all the packages you need for
Django CMS available to be put into your ``INSTALLED_APPS``
setting::

    cd /var/www/django
    django-admin.py startproject wonderwidget
    cd wonderwidget
    python manage.py runserver

Django Projects
---------------

Django projects are, here, typically  layed out in the exact
same way as the Rails projects

For   example  if   we  had   a  django   web  site   called
rainmaker.com, then we'd have some files like::

    /var/www/django/rainmaker/settings.py
    /var/www/django/rainmaker/urls.py
    /var/www/django/rainmaker/manage.py

I  also prefer  to  keep  a public  folder  and yet  another
subfolder of  the public  folder called  media and  keep all
frontend assets like images and  such in the media folder. I
know this is redundant and  adds an extra level of directory
structure but,  again, this  becomes much easier  to reverse
proxy with  Apache if we  keep it  to a single  subfolder of
public.

See my `Django CMS Example on Github <https://github.com/rocksolidwebdesign/Django-CMS-Example>`_

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
    configuration
    tasks

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
