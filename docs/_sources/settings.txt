========
Settings
========

.. _web-server:

Web Server
==========
``server_hostname``
    This is  pretty much the  single most  important setting because  it's where
    you're  aiming the  script.  You should  aim  it at  a  canonical FQDN  like
    ``foobar.myhost.com``.  If  you  want  your  website to  run  on  e.g.  just
    ``myhost.com`` that's fine  this script installs a default  apache host that
    runs on just the top level domain,  so don't set this to just ``myhost.com``
    or this  script will try  to run your server  directly on ``.com``  and that
    won't end well.

``server_domain``
    The top  level domain name  of the server you'll  actually be running  so if
    your hostname is ``rainmaker.wonderwidget.com`` then this setting should
    be ``wonderwidget.com``.

    The domain will be automatically determined  from the hostname so as long as
    you set a nice  canonical FQDN hostname then you don't  actually need to set
    the domain name.

``server_groupname``
    The unix group name under which the  web server runs. You should most likely
    just leave this setting alone unless you  really want your web server to run
    under something other than the default ``www-data`` group.

``webroot_dir``
    The root directory for served file to  the web this directory will be backed
    up if it exists and created if it does not exist

.. _general:

General
=======
``single_user_mode``
    If you are  never going to really  have any other users except  root and the
    web server user, then choose single_user_mode

    This will result in only a single extra user, the deploy user being created.
    The deploy  user will  own and  have full  access to  the webroot  and vhost
    config directories and the deploy user will have full sudo privileges.

    you can still install other team members in deploy mode

``remote_backup_dir``, ``remote_config_dir``
    These  are  the commands  your  deploy  user  can  run, basically  to  allow
    restarting the  web server and  other common  web server related  tasks. You
    should choose a directory that does not yet exist for these settings.

``local_config_dir``
    This is  the path to  your server configuration  files. these files  let you
    customize the resulting server to fit  your tastes e.g. automatic install of
    your  hosts  and  users  just  by filling  out  the  config  directory.  see
    :doc:`configuration` for  an explanation of how  these files are used  and what
    you can do with them.

``local_backup_dir``, ``local_tar_dir``
    These are the local cache files. I call them cache files because, well, they
    don't do much except sit there and look all nice and pretty, packaged up for
    transfer,  just  waiting to  be  uploaded.  Also  none  of these  files  are
    particularly critical because they're generated from the current configs and
    can  be rebuilt  easily  with the  ``regen_configs`` and  ``regen_tarballs``
    tasks respectively.

``create_missing_shell_keys``, ``create_missing_git_keys``
    When it comes  time to create shell  users, usually key pair  access is best
    and  gitolite  actually forces  it  so  if there  aren't  any  keys for  the
    respective shell or gitolite  users in the config dir then  if these are set
    to  true (which  they  are by  default)  then some  keys  will be  generated
    using  ``ssh-keygen``. The  create missing  shell  keys options  is not  yet
    implemented. Only missing git keys are created for now.

.. _user:

User
====
``python_environment_dir``
    The   name   of  the   directory   where   each   user  will   store   their
    virtualenvironments

``main_username``, ``main_password``
    This  is your  main username  - you,  the person  who will  be running  this
    fabfile. so for example 'john' or 'mary' 'superhacker', 'mrcool' or whatever
    username you want.

    If you'r installing via sudo this should be the usernam of the user who hase
    those sudo privileges. for exampl if you're installing to a virtual machin e

``deploy_username``, ``deploy_password``
    The deploy user is your "everything web" user. your deploy user will own all
    the files that belong to your actual websites, your deploy user will be able
    to restart the web server and add vhosts without requiring a password

``team_groupname``, ``team_password``, ``team_users``
    If you have a  list of other users, probably developers  who will need shell
    accounts then

``team_sudo_cmds``
    These  are  the commands  your  deploy  user  can  run, basically  to  allow
    restarting the web server and other common web server related tasks

``vim_config_tarball``
    If you want a custom vim configuration installed for your users, system wide
    you can  use this one, otherwise,  you could of  course put your own  in the
    ``conf/skel`` directory

    If you want your own system wide vim  config just point this to the URL of a
    tarball that contains simply a ``.vim`` folder and ``.vimrc`` file

.. _git:

Git Repositories
================
``gitolite_admin_local``, 
    You will need to checkout the gitolite  admin repo on to your local computer
    to add  the keys for the  deploy user so  that the deploy user  can checkout
    your projects in to your various webroot folders

``gitolite_admin_name``, ``gitolite_admin_email``
    These  settings  are  passed  to ``git  config  --global``  temporarily  and
    previous/current  settings are  saved. After  the gitolite  server has  been
    initialized the original user's git settings are restored.

``gitolite_admin_user``
    This will be the filename of the default gitolite administrator's public key
    when the pub key file is created from the local aka main user's ssh key.

``git_repo_admins``
    Usernames of  the users who are  actually allowed to admin  and maintain the
    repositories and who has access to them

``git_repo_devteam``
    These  are your  actual  developers  who will  need  commit  access to  your
    repositories

``git_hosted_repos``
    This is your list of git repositories
