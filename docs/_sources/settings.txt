========
Settings
========

.. _general:

General
=======
``single_user_mode``
    If you are never going to really have any other users except root
    and the web server user, then choose single_user_mode

    This will result in only a single extra user, the deploy user
    being created. The deploy user will own and have full access to
    the webroot and vhost config directories and the deploy user
    will have full sudo privileges.

    you can still install other team members in deploy mode

``remote_backup_dir``, ``remote_config_dir``
    These are the commands your deploy user can run, basically
    to allow restarting the web server and other common web
    server related tasks. You should choose a directory
    that does not yet exist for these settings.

``local_config_dir``
    This is the path to your server configuration files. these
    files let you customize the resulting server to fit your
    tastes e.g. automatic install of your hosts and users just
    by filling out the config directory. see :doc:`config_dir`
    for an explanation of how these files are used and what
    you can do with them.

.. _web-server:

Web Server
==========
``webroot_dir``
    The root directory for served file to the web
    this directory will be backed up if it exists
    and created if it does not exist

``server_domain``
    The top level domain name of the server you'll actually be running

``server_hostname``
    The specific hostname of the server you'll actually be running

``server_groupname``
    The unix group name under which the web server runs

.. _user:

User
====
``python_environment_dir``
    The name of the directory where each user will
    store their virtualenvironments

``main_username``, ``main_password``
    This is your main username - you, the person who will
    be running this fabfile. so for example 'john' or 'mary'
    'superhacker', 'mrcool' or whatever username you want.

    If you'r installing via sudo this should be the username
    of the user who has those sudo privileges. for example
    if you're installing to a virtual machine

``deploy_username``, ``deploy_password``
    The deploy user is your "everything web" user. your
    deploy user will own all the files that belong to
    your actual websites, your deploy user will be
    able to restart the web server and add vhosts
    without requiring a password

``team_groupname``, ``team_password``, ``team_users``
    If you have a list of other users, probably
    developers who will need shell accounts then

``team_sudo_cmds``
    These are the commands your deploy user can run, basically
    to allow restarting the web server and other common web
    server related tasks

``vim_config_tarball``
    If you want a custom vim configuration installed for your
    users, system wide you can use this one, otherwise, you
    could of course put your own in the ``conf/skel`` directory

    If you want your own system wide vim config just point this 
    to the URL of a tarball that contains simply a 
    ``.vim`` folder and ``.vimrc`` file

.. _git:

Git Repositories
================
``gitolite_admin_local_dir``, ``gitolite_admin_user``, ``gitolite_admin_email``
    You will need to checkout the gitolite admin repo
    on to your local computer to add the keys for the deploy
    user so that the deploy user can checkout your projects
    in to your various webroot folders

``git_repo_admins``
    usernames of the users who are actually allowed to admin and
    maintain the repositories and who has access to them

``git_repo_devteam``
    these are your actual developers who will need commit
    access to your repositories

``git_hosted_repos``
    this is your list of git repositories
