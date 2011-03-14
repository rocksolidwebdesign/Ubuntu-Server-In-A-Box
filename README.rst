About
-----
Ubuntu Server In A Box v0.0.1-ALPHA

A python script to automatically install and set up a full featured
server including web, mail and git repositories.

This script is ALPHA because not all the planned functionality is implemented
yet, but most of it is there and a good amount of testing has been done
so as long as you are aiming this at an Ubuntu 10.10 server you should be good to go.

Quick Install
-------------

To take a quick test drive use this script. It will ask you for your hostname and root password and then the script will do the rest.

    bash < <( curl https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install )

Have a `look at the installer <https://github.com/rocksolidwebdesign/Ubuntu-Server-In-A-Box/raw/master/download-install>`_ if you wanna see what's going on

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
