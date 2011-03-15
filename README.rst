About
-----

Ubuntu Server In A Box v0.0.1-ALPHA

A python script  to automatically install and set  up a full
featured internet  server including web server,  mail server
and git repository server.

How It Works
------------

Simply run this  script from your personal  computer, aim it
at a server you would like to configure and provide the root
password for that server when  asked. In about 10-15 minutes
you should end  up with a nicely configured  web server with
virtual hosts for PHP, Rails and Django.

-------------
Quick Install
-------------

**Please at least read the basic docs before trying the quick install**

`Documentation <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/blob/master/sphinx-docs/index.rst>`_

*Just read the part about requirements and possibly also read
about basic  usage. This should  help clear up  any problems
and make the quick install truly worth of its name :)*

To take a quick test drive use this handy one liner::

    bash < <( curl https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install ) && cd Ubuntu-Server-In-A-Box/maverick_cloud && fab setup

Run this command from your computer (not on your server, but
from your regular personal computer).  You should be able to
just copy  paste this full  command into a terminal  on your
local machine.

Requirements
------------

You might need

* Your local admin password (to install fabric)

You **will definitely need**

* Python 2.x, specifically 2.6 or 2.7
* The python package calle Fabric, or...
* The python package called pip (for installing fabric)

* An standard ssh key pair living at ``~/.ssh/id_rsa`` and ``~/.ssh/id_rsa.pub``
* The ``ssh-copy-id`` utility (Note: Mac OS X users don't have this by default)

* The hostname of a server with Ubuntu 10.10 on it
* The root password for that Ubuntu 10.10 server

Troubleshooting
---------------

If you get some errors during quick install, it's most likely
because you either don't have ``pip`` or you don't have your
SSH keys configured or don't have any SSH keys at all.

-------------------
Further Information
-------------------

Have a `look at the installer <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install>`_ if you wanna see what's going on.

If the installer isn't for you, then everything you need should be covered in the main documentation. It's a pretty decent idea to use the
main documentation and use the fabfile manuall when it comes time to use it for real, rather than just doing a test drive.

* `Documentation <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/blob/master/sphinx-docs/index.rst>`_

    * `Settings <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/blob/master/sphinx-docs/settings.rst>`_
    * `Configuration Directory <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/blob/master/sphinx-docs/config_dir.rst>`_
    * `Tasks <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/blob/master/sphinx-docs/tasks.rst>`_

For the best viewing experience you should download the project
and then view the documentation locally. All the generated documentation
lives in::

    docs/index.html
