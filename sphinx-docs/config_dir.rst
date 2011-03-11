=======================
Configuration Directory
=======================

.. _custom-configuration:

Overview
========

There  is some  custom stuff  going on  with the  web server
that's not completely available through the settings file.

You can add your own users and vhosts simply by adding their
respective files to the configuration directory.

The default config directory is::

    conf/maverick_cloud

but you  can use  your own  in, see  ``local_config_dir`` in
:doc:`settings` The  idea here is  to leave room  for future
distributions and  versions and  particular user,  group and
vhost layouts.

To do anything more complicated than what is available through
these config files you'll need to modify the fab tasks themselves
which you can get a good feel for by reading their descriptive
overviews here: :doc:`tasks`

.. _config-file-templates:

Config File Templates
---------------------

Most of this config magic is actually achieved through the
use of some primitive templating with ``sed``

For most (all?) used config files there is a corresponding
template that includes placeholders for the hostname, so
you can point this at various different computers and 
just let it go.

.. _apache-vhosts:

Apache
======

All the vhost files for apache live in the config folder

``conf/maverick_cloud/apache``

The Hosts You Want
------------------
Just add your extra vhosts to ``vhost_templates`` 

There are actually two directories for vhosts here

* ``sites-available`` This is the folder that actually gets copied
* ``vhost_templates`` These templates are used to generate the actual config files

The ``sites-available`` folder is indeed where the actual vhost
files are copied from when they're put on the server, however
this folder is also cleaned out with the clean commands fab clean
and 

The Hosts You Get Already
-------------------------
* ``default`` Served on the main domain from the setting ``server_domain``
* ``default-ssl`` SSL Served on the main domain from the setting ``server_domain``
* ``default-ssl-nginx`` As above but served on 4433, meant to be reverse proxied with nginx
* ``php_generator`` The PHP script from generatedata.com
* ``proxy_django`` Django dev server available through ``django.server_domain`` e.g. http://django.mysite.com
* ``proxy_rails`` Available through ``rails.server_domain`` e.g. http://rails.mysite.com

Toggling Reverse Proxy Mode
---------------------------
This config is primarily oriented towards
allowing you to quickly and easily switch
back and forth between Apache as the primary server
and Apache being served from behind an Nginx reverse
proxy.

*TODO: A fab task should probably be added for this.*

You will need to be manually logged in to the remote
server with root privileges.

Here's how to toggle the reverse proxying:

* Swap the apache ``ports.conf`` symlink

    * ``/etc/apache2/ports.master.conf`` Runs everything on ports 80 and 443 for SSL
    * ``/etc/apache2/ports.behind_nginx.conf`` Runs everything on ports 8080 and 4433 for SSL

* Swap the apache ssl vhost

    * Choose the relevant option between ``default-ssl`` and
      ``default-ssl-nginx``. *Hint:  if you're  putting Apache
      behind Nginx then choose default-ssl-nginx.*

* Enable the nginx vhosts
* Restart Apache
* Restart Nginx

.. _nginx-vhosts:

Nginx
=====

Configuration style here is basically identical to :ref:`apache-vhosts`

All the vhost files for nginx live in the config folder

``conf/maverick_cloud/nginx``

The Hosts You Get Already
-------------------------
* ``proxy_apache`` Pass all requests through to the proper Apache vhost on port 8080
* ``proxy_apache_ssl`` Runs on SSL and passes all requests through to port 4433
* ``proxy_wsgi`` Django dev server available through ``django.server_domain`` e.g. http://django.mysite.com
* ``proxy_passenger`` Available through ``rails.server_domain`` e.g. http://rails.mysite.com

.. _gitolite-pubkeys:

Gitolite
========

Gitolite is  primarily configured  from within  the settings
file but your gitolite developers and collaborators won't be
added  to the  repos unless  their keys  are present  in the
``conf/maverick_cloud/keys/gitolite`` dir.

Public  keys  follow the  simple  naming  convention of  the
person's username with a  ``.pub`` ending. Simply gather the
public keys  of your users  (or generate them if  they don't
exist,  for that  matter)  and place  them  in the  gitolite
public keys folder ``conf/maverick_cloud/keys/gitolite``.

.. _user-skeleton:

Custom Prefab Users
===================

That awesome  bash prompt comes from  the preconfigured home
directory skeleton in ``conf/maverick_cloud/skel``

All the  files in there  are hidden  so if the  folder looks
empty to you be sure you're showing hidden files.

This config does two main things

* It tries to accomodate RVM and virtualenv
* It tries to accomodate extra login specific customizations

The  first  modification  is   the  addition  of  a  special
conditional   statement   surrounding   the  bulk   of   the
``~/.bashrc``  so that  the rvm  and virtualenv  always work
even for non interactive shells.

This is important if you want future fab tasks to be able to
make use of your rvm and virtualenv settings.

The   second   modification   consists  primarily   of   the
``~/.colors_prompts``  and ``~/.bash_prompt  file`` both  of
which are included by the ``~/.bashrc`` if they exist.

The  ``~/.colors_prompts``  is  in fact  named  clumsily  on
purpose because  it does actually contain  nothing more than
code that defines colors and  prompts. The colors gives us a
flavorful and  powerful menu  from which  to build  a custom
prompt if we wish and it  comes with two prompts already pre
built for you, one for regular user accounts and another for
the root  account that makes  the entire host string  red to
alert  you that  you're root  in  the hopes  that this  will
somehow prevent stupid things from happening.

The  ``~/.bash_prompt`` file  is where  you actually  choose
your prompt by setting the ``$PS1`` environment variable and
just trust me that  the separation between prompt generation
and prompt selection is a good thing.
