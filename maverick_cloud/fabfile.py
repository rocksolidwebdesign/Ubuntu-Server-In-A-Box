import os
from fabric.api import *
from fabric.contrib.console import confirm

print "Welcome to Ubuntu 10.10 - Server In A Box"
print "========================================="

from settings import *

# Download URLs and other settings {{{
rubygems_url = 'http://production.cf.rubygems.org/rubygems'
rubygems_vers = 'rubygems-1.6.2'
rubygems_tarball = 'rubygems-1.6.2.tgz'

pypi_url = 'http://pypi.python.org/packages/source'
pip_vers = 'pip-0.8.2'
pip_url  = pypi_url+'/p/pip/'+pip_vers+'.tar.gz'
pip_md5  = 'df1eca0abe7643d92b5222240bed15f6'

root_host      =  'root@' + server_hostname
gitolite_host  =  'gitolite@'+server_hostname
main_host      =  main_username+'@'+server_hostname
deploy_host    =  deploy_username+'@'+server_hostname

# pseudo inline-function for bash
get_cur_timestamp = '$(date +%Y-%m-%d_%H%M%S)'

# }}}

# MAIN TASKS
################################################################
# Shortcuts - tasks that call the high level generic tasks below

def setup(update=True): # {{{
    """
    Bootstrap an entire server from a blank rackspace Ubuntu 10.10 VPS
    """

    # Preparation
    # ---------------------------------------------------
    # install the root user, config and working dirs
    init_system()

    # this is basically a dependency actually
    # because it has add-apt-repository
    aptget_init()

    # Install security updates
    if update:
        aptget_software_updates()

    aptget_compiler()
    aptget_common_dev_headers()

    # I like to have the latest vim and
    # I like to have a nice vim config
    aptget_vim73()
    install_vim_config()

    # Main Server Setup
    # ---------------------------------------------------
    setup_users()  # setup users in a common group

    setup_server() # includes PHP and MySQL
    setup_python() # includes virtualenv, django and wsgi
    setup_ruby()   # includes rvm, rails and passenger

# }}}
def setup_server(): # {{{
    """
    Installs and configures web, mail and git servers
    """
    install_webroot()
    setup_apache()
    setup_nginx()

    #setup_mail_server()

    setup_git_server()
    #setup_svn_server()

# }}}
def clean_all(): # {{{
    """
    Sort of like make clean but more like uninstall.

    This tries to remove all custom configs, delete 
    all users, and restore original configs from the 
    backups made by this script.
    """
    clean()
    clean_users()
    clean_webroot()
    clean_apache()
    clean_nginx()
    clean_gitolite()

# }}}


# GENERIC TASKS
################################################################
# Tasks that call other tasks that actually get work done

# System Init
def init_system(): # {{{
    """
    Initialialize the bare necessities, i.e. root user etc

    Configures your admin user. Uploads the custom
    home directory skeleton for new users. Creates backup
    and config directories.
    """
    env.host_string = root_host

    regen_configs()
    regen_tarballs()

    init_root_user();

    with settings(hide('warnings'), warn_only=True):
        local('mkdir -p '+local_backup_dir)
        local('mkdir -p '+local_tar_dir)
        run('mkdir -p '+remote_backup_dir)
        run('mkdir -p '+remote_config_dir)

# }}}
def setup_users(): # {{{
    """
    Install basic user accounts
    """
    install_etc_skel()
    install_master_users()
    install_team_users()
    install_team_sudoers()

# }}}

# Web and Mail Servers
def setup_apache(): # {{{
    """
    Installs and configures Apache HTTPD
    """
    aptget_lamp()
    a2enmod_rewrite()
    a2enmod_proxy()

# }}}
def setup_nginx(): # {{{
    """
    Installs and configures nginx
    """
    aptget_nginx()
    install_nginx_config()

# }}}
def setup_mail_server(): # {{{
    aptget_mail_server()
    install_postfix_dovecot_config()

# }}}

# Version Control
def setup_git_server(): # {{{
    """
    Installs and configures web, mail and git servers
    """
    aptget_git_server()
    install_gitolite_config()

# }}}
def setup_svn_server(): # {{{
    """
    Installs and configures subversion and apache svn server
    """
    aptget_svn_server()
    #install_webdav_config()

# }}}

# Python and Ruby
def setup_python(target_host=deploy_host): # {{{
    """
    Installs python, virtualenv and WSGI.

    Also installs the basic django modules system wide using pip. Installs
    virtualenv for the deploy user.
    """

    # install the deps for basic sanity
    install_python_distribute()
    install_python_pip()
    install_python_virtualenv()

    # setup the deploy user with virtualenv
    configure_python_virtualenv(target_host)

    # install the wsgi apache module and the standalone uwsgi
    aptget_mod_wsgi()
    aptget_uwsgi()

    # install the common pip modules for django apps like django-cms
    install_sys_djangocms()

# }}}
def setup_ruby(target_host=deploy_host): # {{{
    """
    Installs rails and passenger.
    
    Installs  system  ruby   with  compatibility  rails,  recent
    rubygems and rvm for deploy user with latest rails.
    """
    aptget_ruby()

    # latest gems, but system wide
    install_rubygems()

    # install rails server for apache
    install_rails_server()
    install_mod_passenger_gem()

    # rvm installs
    install_rvm(target_host)
    install_rvm_rails_server(target_host)

# }}}

# }}}


# REAL TASKS
################################################################
# Stuff that actually does the work

# Core Configuration
# Users {{{
# root
def init_root_user(): # {{{
    """
    Configure a root user account for convenient access, requires root password.

    Installs your SSH key for the root user. Uploads the custom
    home directory skeleton for new users. Creates backup
    and config directories.
    """
    env.host_string = root_host

    local('ssh-copy-id ' + root_host)

    # these both use root by default
    add_prompt_to_user()
    select_prompt()

# }}}
def clean_root_user(): # {{{
    """
    Try to clean up any of the custom user configurations for root

    Remove the custom vim configuration if it exists. Remove sudoers file.
    Delete various other shell customization files.
    """
    env.host_string = root_host

    run('rm -rf .vim .vimrc .viminfo .ssh .colors_prompts .bash_prompt')
    run('if [ -e ~/.bashrc.bak ]; then rm -rf ~/.bashrc; mv ~/.bashrc.bak ~/.bashrc; fi')

# }}}

# users
def install_master_users(): # {{{
    """
    Install deploy and main users depending on ``single_user_mode``
    """
    env.host_string = root_host

    if single_user_mode:
        add_custom_user(deploy_username, deploy_password)

        # same login as root
        clone_root_pubkey(deploy_username, '/home/'+deploy_username)

        # root permissions
        run('adduser '+deploy_username+' sudo')

    else:
        add_custom_user(deploy_username, deploy_password)
        add_custom_user(main_username, main_password)

        # same login as root
        clone_root_pubkey(deploy_username, '/home/'+deploy_username)
        clone_root_pubkey(main_username, '/home/'+main_username)

        # root permissions
        run('adduser '+main_username+' sudo')

# }}}
def clean_master_users(): # {{{
    """
    Remove the deploy and main user accounts
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        run('deluser '+deploy_username)
        run('rm -rf /home/'+deploy_username)

        if not single_user_mode:
            run('deluser '+main_username)
            run('rm -rf /home/'+main_username)

# }}}

# team
def install_team_users(): # {{{
    """
    Setup team user accounts for each member

    If this is a shared workgroup server with multiple user
    accounts, then set up each initial user account with
    proper group and permissions to work on the same files
    """
    env.host_string = root_host

    run('addgroup '+team_groupname)

    run('adduser '+deploy_username+' '+team_groupname)
    run('adduser '+deploy_username+' '+server_groupname)
    if single_user_mode:
        run('adduser '+server_groupname+' '+team_groupname)
    else:
        run('adduser '+main_username+' '+team_groupname)
        run('adduser '+main_username+' '+server_groupname)

    for name in team_users:
        add_custom_user(name, team_password)
        run('adduser '+name+' '+server_groupname)
        run('adduser '+name+' '+team_groupname)

# }}}
def clean_team_users(): # {{{
    """
    Remove any team user accounts
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        run('deluser '+deploy_username)
        run('deluser '+main_username)
        run('rm -rf /home/'+deploy_username)
        run('rm -rf /home/'+main_username)

        for name in team_users:
            run('deluser '+name)
            run('rm -rf /home/'+name)

# }}}

# sudoers
def install_team_sudoers(): # {{{
    """
    Give team members some limited webserver related priviliges

    Install our own custom sudoers config for the team to
    allow team members to stop and start the web server.
    """
    env.host_string = root_host

    alias_list  = ','.join(team_sudo_cmds)
    cmd_alias   = 'Cmnd_Alias WEB_SERVER_CMDS = '+alias_list
    sudoer_line = '%'+team_groupname+' ALL=(ALL) NOPASSWD: WEB_SERVER_CMDS'

    run("echo '"+cmd_alias+"' > /etc/sudoers.d/"+team_groupname)
    run("echo '"+sudoer_line+"' >> /etc/sudoers.d/"+team_groupname)
    run("chmod 440 /etc/sudoers.d/"+team_groupname)

# }}}
def clean_team_sudoers(): # {{{
    """
    Remove the extra team privileges
    """
    env.host_string = root_host

    run('if [ -e /etc/sudoers.d/'+team_groupname+' ]; then rm -rf /etc/sudoers.d/'+team_groupname+'; fi')
# }}}

# home skeleton
def install_etc_skel(): # {{{
    """
    Uploads the new user skeleton directory to the remote_config_dir
    """
    env.host_string = root_host

    put(local_tar_dir+'/skel.tar.gz', remote_config_dir)
    with cd(remote_config_dir):
        run('tar -zxf skel.tar.gz')
        run('rm -rf skel.tar.gz')

# }}}
def clean_etc_skel(): # {{{
    """
    Removes the user configuration skeleton dir

    Removes the skeleton from the config directory. Maybe don't need
    this since we've got a clean config task already?
    """
    env.host_string = root_host

    run('rm -rf '+remote_config_dir+'/skel')

# }}}

# vim config
def install_vim_config(): # {{{
    """
    Install custom vim configuration

    Try to install our custom vim configuration in the main system 
    for all users.
    """
    env.host_string = root_host

    if len(vim_config_tarball_url):
        # get nice vim configuration
        with settings(hide('warnings'), warn_only=True):
            if run('wget '+vim_config_tarball_url).succeeded:
                filename = os.path.basename(vim_config_tarball_url)
                run('tar -zxf '+filename)

                run('rm -rf /usr/share/vim/vimfiles')

                # install the vim configuration system wide
                run('mv .vimrc /etc/vim/vimrc.local')
                run('mv .vim /usr/share/vim/vimfiles')

                # cleanup
                run('rm -rf '+filename)

# }}}
def clean_vim_config(): # {{{
    """
    Delete the custom system wide vim config files if they exist
    """
    env.host_string = root_host

    vimfiles = '/usr/share/vim/vimfiles'
    vimrc    = '/etc/vim/vimrc.local'

    run('if [ -d '+vimfiles+' ]; then rm -rf '+vimfiles+'; fi')
    run('if [ -d '+vimrc+' ]; then rm -rf '+vimrc+'; fi')

    run('if [ ! -e /usr/share/vim/vimfiles ]; then ln -s /etc/vim /usr/share/vim/vimfiles; fi')
# }}}

# }}}
# Servers {{{
def backup_webroot(): # {{{
    """
    Backs up the webroot if it exists.

    Title should be self explanatory, this backs up the main server
    webroot directory if it exists.
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        if len(webroot_dir) and run('[ -e '+webroot_dir+' ]').succeeded:
            with cd(webroot_dir):
                run('tar -czf '+remote_backup_dir+'/webroot.tar.gz ./')
# }}}
def restore_webroot(): # {{{
    """
    Restore original webroot from backup if the backup exists
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        if run('[ -e '+remote_backup_dir+'/webroot.tar.gz ]').succeeded:
            run('rm -rf '+webroot_dir)
            run('mkdir -p '+webroot_dir)
            run('mv '+remote_backup_dir+'/webroot.tar.gz '+webroot_dir)
            with cd(webroot_dir):
                run('tar -zxf webroot.tar.gz')
                run('rm -rf webroot.tar.gz')
# }}}
def install_webroot(): # {{{
    """
    Create initial webroot directory layout for Apache, Django and Rails

    Sets up the initial outline for the main web server root directory.
    The way I like it is split in to three sections one for apache/php
    and two others for python and ruby (rails and django) projects.

    The currently installed folders are

    * ``webroot/apache``
    * ``webroot/django``
    * ``webroot/rails``
    """
    env.host_string = root_host

    backup_webroot()
    run('if [ -e "'+webroot_dir+'" ]; then rm -rf '+webroot_dir+'; fi')


    run('mkdir -p '+webroot_dir+'/django')
    run('mkdir -p '+webroot_dir+'/rails')

# }}}
def backup_apache_config(): # {{{
    """
    Backs up the apache config to the backup directory
    """
    env.host_string = root_host
    with settings(hide('warnings'), warn_only=True):
        if run('[ ! -e '+remote_backup_dir+'/apache2.tar.gz ]').succeeded:
            with cd('/etc'):
                run('tar -czf '+remote_backup_dir+'/apache2.tar.gz apache2')
# }}}
def restore_apache_config(): # {{{
    """
    Restore original apache config from backup if the backup exists
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        if run('[ -e '+remote_backup_dir+'/apache2.tar.gz ]').succeeded:
            # remove custom apache config
            run('rm -rf /etc/apache2')
            run('mv '+remote_backup_dir+'/apache2.tar.gz /etc')
            with cd('/etc'):
                run('tar -zxf apache2.tar.gz')
                run('rm -rf apache2.tar.gz')
# }}}
def install_apache_config(): # {{{
    """
    Install apache vhosts and custom "behind nginx" switch

    Copies the customized and templated vhosts from
    your local config dir to the actual web server and
    then restarts.  This also sets up a symlink for
    ports to allow switching between having apache
    as the master server and having apache behind an
    nginx reverse proxy. Sets up permissions for
    team sharing of the vhost configs.
    """
    env.host_string = root_host

    backup_apache_config()

    # setup files for switching between nginx and apache
    put(local_config_dir+'/apache/ports.master.conf', '/etc/apache2')
    put(local_config_dir+'/apache/ports.behind_nginx.conf', '/etc/apache2')
    run('rm -rf /etc/apache2/ports.conf')
    run('ln -s /etc/apache2/ports.master.conf /etc/apache2/ports.conf')

    # install vhosts
    run('rm -rf /etc/apache2/sites-available/*')
    run('rm -rf /etc/apache2/sites-enabled/*')
    put(local_tar_dir+'/apache/sites-available.tar.gz', '/etc/apache2')
    with cd('/etc/apache2'):
        run('tar -zxf sites-available.tar.gz')
        run('rm -rf sites-available.tar.gz')

    # allow team and or admins to add and edit vhosts
    if single_user_mode:
        configure_open_share(deploy_username, team_groupname, '/etc/apache2/sites-available')
    else:
        configure_restricted_share('root', team_groupname, '/etc/apache2/sites-available')

    # enable all the vhosts
    with cd('/etc/apache2/sites-enabled'):
        run('find ../sites-available/ -type f -exec ln -s "{}" . \;')

        # by default we don't run apache behind nginx for now
        run('rm -rf default-ssl-nginx')

    # at least install skeleton outline dirs for the vhosts
    run('mkdir -p '+webroot_dir+'/apache/localhost/public')
    run('mkdir -p '+webroot_dir+'/apache/generator.'+server_domain+'/public')
    run('mkdir -p '+webroot_dir+'/apache/django.'+server_domain+'/public')
    run('mkdir -p '+webroot_dir+'/apache/rails.'+server_domain+'/public')

    # set this up later?
    upload_website_apache_localhost()

    run('service apache2 restart')

# }}}
def backup_nginx_config(): # {{{
    """
    Backs up the nginx configuration dir into the backup directory
    """
    env.host_string = root_host

    if run('[ ! -e '+remote_backup_dir+'/nginx.tar.gz ]').succeeded:
        with cd('/etc'):
            run('tar -czf '+remote_backup_dir+'/nginx.tar.gz nginx')
# }}}
def restore_nginx_config(): # {{{
    """
    Restore original nginx config from backup if the backup exists
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        if run('[ -e '+remote_backup_dir+'/nginx.tar.gz ]').succeeded:
            # remove custom apache config
            run('rm -rf /etc/nginx')
            run('mv '+remote_backup_dir+'/nginx.tar.gz /etc')
            with cd('/etc'):
                run('tar -zxf nginx.tar.gz')
                run('rm -rf nginx.tar.gz')
# }}}
def install_nginx_config(): # {{{
    """
    Install nginx vhosts suitable for reverse proxying Apache

    Copies the customized and templated vhosts from
    your local config dir to the actual web server and
    then restarts. Sets up permissions for team sharing
    of the vhost configs. For now these are not turned on
    by default.
    """
    env.host_string = root_host

    backup_nginx_config()

    # setup vhosts
    run('rm -rf /etc/nginx/sites-available/*')
    run('rm -rf /etc/nginx/sites-enabled/*')
    put(local_tar_dir+'/nginx/sites-available.tar.gz', '/etc/nginx')
    with cd('/etc/nginx'):
        run('tar -zxf sites-available.tar.gz')
        run('rm -rf sites-available.tar.gz')

    if single_user_mode:
        configure_open_share(deploy_username, team_groupname, '/etc/nginx/sites-available')
    else:
        configure_restricted_share('root', team_groupname, '/etc/nginx/sites-available')

    # don't turn on nginx for now
    #with cd('/etc/nginx/sites-enabled'):
    #    run('find ../sites-available/ -type f -exec ln -s "{}" . \;')

    run('service nginx restart')

# }}}
def install_gitolite_config(): # {{{
    """
    Initializes and sets up the gitolite server

    Installs and a basic git server adds your repos and gives
    your developers access to those repos. There's no backup
    fab task because there are never any repos to begin with,
    you may however wish to run the ``clean_gitolite`` task
    which deletes any and all files that the gitolite setup
    adds to its home directory.
    """
    env.host_string = deploy_host

    # create key pair for deploy user for doing checkouts
    with settings(hide('warnings'), warn_only=True):
        run('no | ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa')
    deploy_ssh_rsa = run('cat ~/.ssh/id_rsa.pub')
    local_ssh_rsa  = local('cat ~/.ssh/id_rsa.pub', capture=True)

    # setup gitolite user and repositories
    env.host_string = root_host

    # gitolite is very adamant in its desires to run as its own independent
    # user which is added when gitolite is installed. thusly we must first
    # enable shell access so we can log in as the gitolite user
    clone_root_pubkey('gitolite', '/var/lib/gitolite')

    # set git user config on the server itself for the user we'll be working as
    env.host_string = gitolite_host
    run('git config --global user.name "'+gitolite_admin_name+'"')
    run('git config --global user.email '+gitolite_admin_email)

    # because gitolite makes some assumptions about how we'll be using ssh
    # it does not like it if there is already a .ssh folder so we must
    # delete the .ssh dir before running gl-setup to install
    # the gitolite configuration.
    #
    # Deleting the .ssh folder, obviously will lock us out, but the gitolite
    # setup script by default requires a public key and will load this
    # key so users can do repository checkouts. Gitolite does not, however
    # grant shell access to its user account, so we must do that explicitly.
    #
    # We must do all these things at once to prevent being locked out between
    # commands because fabric retrieves a new connection for each command
    run("echo '"+local_ssh_rsa+"' > ~/"+gitolite_admin_user+".pub")
    run('rm -rf .ssh && gl-setup ~/'+gitolite_admin_user+'.pub && yes "" | /usr/share/gitolite/gl-tool shell-add ~/'+gitolite_admin_user+'.pub')

    # save original config information
    git_local_name  = local('git config --global --get user.name', capture=True)
    git_local_email = local('git config --global --get user.email', capture=True)

    local('# SAVED CONFIG: '+git_local_name+' '+git_local_email)

    local('git config --global user.name "'+gitolite_admin_name+'"')
    local('git config --global user.email '+gitolite_admin_email)

    # make a local dir for checking out the gitolite admin settings
    local('mkdir -p '+gitolite_admin_local)
    local('rm -rf '+gitolite_admin_local+'/gitolite-admin')

    with lcd(gitolite_admin_local):
        local('git clone '+gitolite_host+':gitolite-admin')

    with lcd(gitolite_admin_local+'/gitolite-admin'):
        # and add keys for users
        local("echo '"+deploy_ssh_rsa+"' > keydir/"+deploy_username+".pub")

    local('rm -rf '+gitolite_admin_local+'/gitolite-admin/conf/gitolite.conf')
    local('cp '+local_config_dir+'/gitolite.conf '+gitolite_admin_local+'/gitolite-admin/conf')
    local('cp '+local_config_dir+'/gitolite_repos.conf '+gitolite_admin_local+'/gitolite-admin/conf')

    for name in git_repo_devteam:
        with settings(hide('warnings'), warn_only=True):
            if local('[ ! -e '+local_config_dir+'/keys/gitolite/'+name+'.pub ]').succeeded:
                local('ssh-keygen -t rsa -N "" -f '+local_config_dir+'/keys/gitolite/'+name)

            local('cp '+local_config_dir+'/keys/gitolite/'+name+'.pub '+gitolite_admin_local+'/gitolite-admin/keydir')

    with lcd(gitolite_admin_local+'/gitolite-admin'):
        local('git add .')
        local('git commit -a -m "Added users"')
        local('git push origin master')

    # restore original config information
    local('git config --global user.name "'+git_local_name+'"')
    local('git config --global user.email '+git_local_email)

# }}}
def clean_gitolite_config(): # {{{
    """
    Delete the gitolite specific files for repositories and config and such
    """
    env.host_string = root_host

    with cd('/var/lib/gitolite'):
        run('rm -rf .gitolite .gitolite.rc projects.list repositories .cache *.pub .ssh')

# }}}
def upload_website_apache_localhost(host=root_host): # {{{
    """
    Uploads the actual publicly accessible files for the default localhost

    Installs a set of skeleton files for the default vhost, aka
    localhost, for apache. Right now this is basically just ``info.php``
    which has a call to ``phpinfo()`` and a default index file
    so you can see that the server is working.
    """
    env.host_string = host

    run('mkdir -p '+webroot_dir+'/apache/localhost')
    put(local_tar_dir+'/apache/localhost/public.tar.gz', webroot_dir+'/apache/localhost')
    with cd(webroot_dir+'/apache/localhost'):
        run('tar -zxf public.tar.gz')
        run('rm -rf public.tar.gz')
# }}}
#def upload_website_apache_generatedata(): # {{{
#    """
#    Uploads the generatedata PHP app to its own vhost

#    Installs the files for the generatedata PHP script in a virtual host.
#    """
#    run('mkdir -p '+webroot_dir+'/apache/generatedata.'+server_domain+'')
#    put(local_tar_dir+'/apache/generatedata.'+server_domain+'/public.tar.gz', webroot_dir+'/apache/generatedata.'+server_domain+'')
#    with cd(webroot_dir+'/apache/generatedata.'+server_domain+''):
#        run('tar -zxf public.tar.gz')
#        run('rm -rf public.tar.gz')
#
#    configure_open_share(deploy_username, server_groupname, webroot_dir)
#
## }}}

# }}}
# Aptget {{{
def aptget_software_updates(): # {{{
    """
    Download and install the latest security patches for Ubuntu.
    """
    env.host_string = root_host
    run('apt-get update')
    run('yes | apt-get upgrade')

# }}}
def aptget_compiler(): # {{{
    """
    We'll need a compiler and basic build tools if we want
    to compile software.
    """
    env.host_string = root_host
    run('yes | apt-get install build-essential gcc g++ make')

# }}}
def aptget_common_dev_headers(): # {{{
    """
    Install database, image and xml dev headers for compiling modules

    Common PHP, Ruby and python modules want some various dev
    headers around if we're going to compile from scratch
    """
    env.host_string = root_host
    run('yes | apt-get install libmysqlclient-dev libpq-dev libmagickwand-dev libxml2-dev libxslt1-dev python-dev ruby-dev libcurl4-openssl-dev')

# }}}
def aptget_git_server(): # {{{
    """
    Install git, the gitolite repo server and the gitweb frontend browser
    """
    env.host_string = root_host
    run('yes | apt-get install git gitolite gitweb')

# }}}
def aptget_svn_server(): # {{{
    """
    Install subversion and apache plugin
    """
    env.host_string = root_host
    run('yes | apt-get install subversion libapache2-svn')

# }}}
def aptget_databases(): # {{{
    """
    Install the common databases: MySQL, Postgres and SQLite
    """
    run('yes | apt-get install mysql-server mysql-client postgresql sqlite sqlite3')

# }}}
def aptget_lamp(): # {{{
    """
    Install Apache along with CGI and PHP modules
    
    And a whole ton of common PHP extensions that should 
    be good enough for running common fairly advanced 
    software like Magento
    """
    env.host_string = root_host
    run('yes | apt-get install apache2 apache2-dev libapache2-mod-fcgid php5 php5-dev php5-cli php-pear php-apc php5-sqlite php5-mysql php5-pgsql php5-curl php5-imagick php5-gd php5-mcrypt php5-xdebug php5-xmlrpc php5-xsl')

# }}}
def a2enmod_rewrite(): # {{{
    """
    Enable the Rewrite module
    """
    env.host_string = root_host
    run('a2enmod rewrite')
    run('service apache2 restart')

# }}}
def a2enmod_passenger(): # {{{
    """
    Enable the Passenger module for serving Ruby apps
    """
    env.host_string = root_host
    run('a2enmod passenger')
    run('service apache2 restart')

# }}}
def a2enmod_proxy(): # {{{
    """
    Enable the Proxy and Proxy HTTP modules
    """
    env.host_string = root_host
    run('a2enmod proxy')
    run('a2enmod proxy_http')
    run('service apache2 restart')

# }}}
def aptget_ruby(): # {{{
    """
    Install the Ubuntu-packaged ruby from the main system including dev headers
    """
    env.host_string = root_host
    run('yes | apt-get install ruby ri ruby-dev')

# }}}
def aptget_passenger(): # {{{
    """
    Install and enable the apache Passenger module for running ruby apps
    """
    env.host_string = root_host
    run('yes | apt-get install libapache2-mod-passenger')
    run('a2enmod passenger')
    run('service apache2 restart')

# }}}
def aptget_mod_wsgi(): # {{{
    """
    Install and enable the apache WSGI module for running python apps
    """
    env.host_string = root_host
    run('yes | apt-get install libapache2-mod-wsgi')
    run('a2enmod wsgi')
    run('service apache2 restart')

# }}}
def aptget_nginx(): # {{{
    """
    Update to the lates nginx repo and install nginx
    """
    env.host_string = root_host
    run('add-apt-repository ppa:nginx/development')
    run('yes | apt-get update')
    run('yes | apt-get install nginx-common nginx-extras')

# }}}
def aptget_uwsgi(): # {{{
    """
    Update to the latest uwsgi repo and install uwsgi
    """
    env.host_string = root_host
    run('add-apt-repository ppa:uwsgi/release')
    run('yes | apt-get update')
    run('yes | apt-get install uwsgi-python')

# }}}
def aptget_mail_server(): # {{{
    """
    Install the commonly desired tools for setting up a mail server
    """
    env.host_string = root_host
    run('yes | apt-get install dovecot-postfix postfix-doc postfix-mysql')

# }}}
def aptget_vim73(): # {{{
    """
    Install the latest vim which right now is 7.3

    Update to the latest vim repo and install the latest vim
    plus a couple common utilities that my vim config uses:

    * ``ctags`` exuberrant ctags
    * ``par`` the paragraph formatter
    """
    env.host_string = root_host
    run('add-apt-repository ppa:ubuntu-backports-testers/ppa')
    run('yes | apt-get update')
    run('yes | apt-get install vim ctags par')

# }}}
def aptget_init(): # {{{
    """
    Updates package list and installs: locate, tmux, add-apt-repository

    Some   various  handy   things   I   alwas  want,   plus
    ``add-apt-repository`` is currently  a dependency of the
    ubuntu packaging tasks, so do  not remove that or remove
    calls to this function
    """
    env.host_string = root_host
    run('apt-get update')
    run('yes | apt-get install python-software-properties mlocate tmux')
# }}}

# }}}
# Python {{{
def install_python_distribute(): # {{{
    """
    Installs the "distribute" python package, a setuptools clone

    Install setuptools so we can build pip and other packages.
    I prefer using distribute.
    """
    env.host_string = root_host
    run('curl -O http://python-distribute.org/distribute_setup.py')
    run('python distribute_setup.py')

# }}}
def install_python_pip(): # {{{
    """
    Download and install a recent version of the pip utility
    """
    env.host_string = root_host
    the_file = pip_vers + '.tar.gz'
    run('wget ' + pip_url)

    with settings(warn_only=True):
        md5_compute = run('md5sum '+the_file)
        md5_string  = pip_md5+'  '+the_file
        result      = run('[ "'+md5_compute+'" = "'+md5_string+'" ]')
    if result.failed and not confirm("Bad pip tarball. Continue anyway?"):
        abort("Aborting at user request.")

    run('tar -zxf ' + the_file)
    with cd(pip_vers):
        run('python setup.py install')

# }}}
def install_python_virtualenv(): # {{{
    """
    Install virtualenv and virtual env wrapper from pip
    """
    env.host_string = root_host
    run('pip install virtualenv virtualenvwrapper')
# }}}
def configure_python_virtualenv(target_host): # {{{
    """
    Add virtualenv capabilites to this user.
    
    Mostly this just adds the config settings to the ~/.bashrc to
    provide access to ``workon`` and ``mkvirtualenv``. This is
    only applicable on a per user basis.
    """
    env.host_string = target_host
    run('mkdir -p '+python_environment_dir)
    run('echo >> ~/.bashrc')
    run('echo \'export WORKON_HOME='+python_environment_dir+'\' >> ~/.bashrc')
    run('echo \'export VIRTUALENV_USE_DISTRIBUTE=1\' >> ~/.bashrc')
    run('echo \'source /usr/local/bin/virtualenvwrapper.sh\' >> ~/.bashrc')

# }}}
def install_sys_djangocms(): # {{{
    """
    Download and install Django CMS with pip

    Add rvm capabilites to this user. Mostly this
    just adds the config settings to the ~/.bashrc to
    provide access to ``rvm``. This is only applicable
    on a per user basis.
    """
    env.host_string = root_host

    run('pip install '+' '.join(djangocms_deps))

# }}}
def install_env_djangocms(target_host=deploy_host, virtualenv='djangocms_test'): # {{{
    """
    Download and install RVM (the Ruby Version Manager)

    Add rvm capabilites to this user. Mostly this
    just adds the config settings to the ~/.bashrc to
    provide access to ``rvm``. This is only applicable
    on a per user basis.
    """
    env.host_string = target_host

    with run('. ~/Envs/'+virtualenv+'/bin/activate'):
        run('pip install '+' '.join(djangocms_deps))

# }}}

# }}}
# Ruby {{{
def install_rubygems(): # {{{
    """
    Download and install the latest rubygems system wide
    """
    env.host_string = root_host

    with settings(hide('warnings'), warn_only=True):
        if run('wget '+rubygems_url+'/'+rubygems_tarball).succeeded:
            run('tar -zxf '+rubygems_tarball)
            with cd(rubygems_vers):
                run('ruby setup.rb')
                run('ln -s /usr/bin/gem1.8 /usr/bin/gem')

# }}}
def install_rails_server(): # {{{
    """
    Download and install rails 2.3.8 system wide

    Ruby  1.8  with  rails   2.3.8  keeps  the  main  server
    compatible with radiantcms. Latest ruby and rails can be
    found in rvm for the deploy user.
    """
    env.host_string = root_host

    run('gem install passenger')
    run('gem install rails --version 2.3.8')
    run('gem install '+' '.join(rails_gem_deps))

# }}}
def install_mod_passenger_gem(): # {{{
    """
    Download and install the latest passenger gem into the system apache
    """
    env.host_string = root_host

    run('passenger-install-apache2-module -a')
    run('passenger-install-apache2-module --snippet | grep --color=none ^LoadModule > /etc/apache2/mods-available/passenger.load')
    run('passenger-install-apache2-module --snippet | grep --color=none ^Passenger > /etc/apache2/mods-available/passenger.conf')

    run('a2enmod passenger')
    run('service apache2 restart')

    # requires recompilation and so, means we can't use the ubuntu packaged nginx
    #run('passenger-install-nginx-module')
    #run('service nginx restart')

# }}}
def install_rvm(target_host=deploy_host): # {{{
    """
    Download and install RVM (the Ruby Version Manager) for a given user

    Add rvm capabilites to this  user. Mostly this just adds
    the config  settings to the ~/.bashrc  to provide access
    to ``rvm``. This is only applicable on a per user basis.
    """
    env.host_string = target_host

    run('bash < <( curl http://rvm.beginrescueend.com/releases/rvm-install-head )')
    run('echo >> .bashrc')
    run('echo \'[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"\' >> .bashrc')

# }}}
def install_rvm_rails_server(target_host=deploy_host): # {{{
    """
    Install Ruby 1.9.2 and Rails 3.x from rvm for the given user

    Also installs a number of pretty standard desirably gems. Don't bother
    with the XSLT lib because it's broken in 1.9.
    """
    env.host_string = target_host

    run('rvm install 1.9.2')
    with prefix('rvm 1.9.2'):
        run('gem install passenger rails '+' '.join(rails_gem_deps[:-1]))

# }}}

# }}}


# SUPPORT TASKS
################################################################
# Modular and repeatable helpers that other tasks can use

# Generate Configs
def regen_configs(): # {{{
    """
    Generate server config files, like vhosts, based on templates.

    Generate the config files from their respective templates. Also
    the list of gitolite repos is built from the settings array ``git_hosted_repos``

    Currently this list of templates includes

    * ``apache/vhost_templates``
    * ``nginx/vhost_templates``
    * ``gitolite.conf.sample``
    """
    args = '_ "{}"'

    replacements = 'sed -e "s/SERVERDOMAINNAME/'+server_domain+'/" | sed -e "s#SERVERWEBROOT#'+webroot_dir+'#"'
    cmd = 'fname=$(echo $1 | sed "s#.*/##"); cat $fname | '+replacements+' > ../sites-available/$fname'
    with lcd(local_config_dir+'/apache/vhost_templates'):
        local("find . -type f -exec bash -c '"+cmd+"' "+args+" \;")

    with lcd(local_config_dir+'/nginx/vhost_templates'):
        local("find . -type f -exec bash -c '"+cmd+"' "+args+" \;")

    replacements = 'sed -e "s/SERVERADMINS/'+' '.join(git_repo_admins)+'/" | sed -e "s/SERVERDEVTEAM/'+' '.join(git_repo_devteam)+'/"'
    local('cat '+local_config_dir+'/gitolite.conf.sample | '+replacements+' > '+local_config_dir+'/gitolite.conf')

    local("echo '# repos' > "+local_config_dir+"/gitolite_repos.conf")
    for repo in git_hosted_repos:
        local("echo >> "+local_config_dir+"/gitolite_repos.conf")
        local("echo 'repo "+repo+"' >> "+local_config_dir+"/gitolite_repos.conf")
        local("echo 'RW+  = @devteam' >> "+local_config_dir+"/gitolite_repos.conf")

# }}}
def regen_tarball(srcdir, source): # {{{
    """
    Generate a tarball of a config dir

    This is a helper function for regenerating all the config tarballs for upload

    Files end up in

    * ``conf/tarballs``
    """

    target_dir = os.path.join(local_tar_dir, srcdir)
    target     = os.path.join(target_dir, source+'.tar.gz')
    srcdir     = os.path.join(local_config_dir, srcdir)

    local('if [ -e '+target+' ]; then mv '+target+' '+target+'.tar.gz.bak.'+get_cur_timestamp+'; fi')
    local('mkdir -p '+target_dir)

    with settings(hide('warnings'), warn_only=True):
        if local('[ -e "'+srcdir+'" ]').succeeded:
            with lcd(srcdir):
                local('tar -czf '+target+' '+source+'')

def regen_tarballs(): # {{{
    """
    Tarball the config tarballs for ease of upload

    This script uploads a number of tarballs that are used to configure
    the server with the settings you want. This Method freshly regenerates
    those tarballs from scratch and keeps timestamped backups of any
    tarballs that might already exist. The current tarballs are

    * ``conf/skel``
    * ``conf/apache/localhost/public``
    * ``conf/apache/sites-available``
    * ``conf/nginx/sites-available``
    """
    local('mkdir -p '+local_backup_dir)
    local('mkdir -p '+local_tar_dir)

    configs = [
        {'source': 'skel',            'srcdir': ''},
        {'source': 'public',          'srcdir': 'apache/localhost'},
        {'source': 'sites-available', 'srcdir': 'apache'},
        {'source': 'sites-available', 'srcdir': 'nginx'},
    ]

    import os
    for config in configs:
        regen_tarball(source=config['source'], srcdir=config['srcdir'])

# }}}
def docs(): # {{{
    """
    Regenerate the sphinx based documentation for this fabfile
    """
    with lcd('../sphinx-docs'):
        local('rm -rf ../docs/ && yes "" | sphinx-build -b html . ../docs')

# }}}

# }}}

# Tests 
def test_local(): # {{{
    """
    Test echo on localhost. Reports the git user settings and the environment $SHELL variable.
    """
    git_username = local('git config --global --get user.name', capture=True)
    local("echo 'Git User: "+git_username+"'")
    local('echo "Current Shell: $SHELL"')

# }}}
def test_remote(user='root'): # {{{
    """
    Test a remote host, takes user account login name as a single argument
    """
    env.host_string = user+'@'+server_fqdn

    run('rvm')
    git_username    = run('git config --global --get user.name')
    run("echo 'Git User: "+git_username+"'")
    run('echo "Current Shell: $SHELL"')

# }}}

# Cleaning
def clean(keys=False): # {{{
    """
    This is more like make clean. This deletes all the custom config files generated by regen_configs()
    """

    print '''
    fab clean
        WARNING, this task will delete your 
        generated configs and backup files

    '''
    if not confirm('Are you sure you want to do this?'):
        return

    # local cache
    local('rm -rf '+local_tar_dir)
    local('rm -rf '+local_backup_dir)

    # vhosts
    local('rm -rf '+local_config_dir+'/apache/sites-available/*')
    local('rm -rf '+local_config_dir+'/nginx/sites-available/*')

    # git
    local('rm -rf '+local_config_dir+'/gitolite.conf')
    local('rm -rf '+local_config_dir+'/gitolite_repos.conf')

    # compiled python files
    local('find ../ -type f -iname "*.pyc" -exec rm -rf "{}" +')

    if keys:
        local('rm -rf '+local_config_dir+'/keys/gitolite/*')
        local('rm -rf '+local_config_dir+'/keys/shell/*')

# }}}
def clean_remote_config_dir(): # {{{
    """
    Remove the main configuration uploads dir
    """
    env.host_string = root_host

    run('if [ -e '+remote_config_dir+' ]; then rm -rf '+remote_config_dir+'; fi')
# }}}
def clean_remote_backup_dir(): # {{{
    """
    Remove the main remote backup dir
    """
    env.host_string = root_host

    run('if [ -e '+remote_backup_dir+' ]; then rm -rf '+remote_backup_dir+'; fi')
# }}}

# User and Permissions Helpers
def configure_restricted_share(user, group, d): # {{{
    """
    Set group ownership of a directory

    This is the case in which we want users to be able to add
    files to a directory but not automatically be able to edit
    or change the contents of that directory.
    """
    env.host_string = root_host

    run('chown '+user+'.'+group+' '+d)
    run('chmod g+w '+d)

# }}}
def configure_open_share(user, group, d): # {{{
    """
    Recursively set and enforce group ownership of a directory

    This is the case where we want all users of the group
    to always be able to have write permissions on all files
    in this directory, even new files created by other people.
    """
    env.host_string = root_host

    run('chown -R '+user+'.'+group+' '+d)
    run('chmod -R g+w '+d)
    run('find '+d+' -type d -exec chmod g+s "{}" +')

# }}}
def clone_root_pubkey(user, home): # {{{
    """
    Copy pubkey from root to avoid password prompt

    Copy our current key from the root user to another user to
    avoid the need for a password when logging in.
    """
    env.host_string = root_host

    run('mkdir -p '+home+'/.ssh')
    run('cp /root/.ssh/authorized_keys '+home+'/.ssh/authorized_keys')
    run('chown -R '+user+'.'+user+' '+home+'/.ssh')
# }}}
def add_custom_user(user, passw, fancy=True): # {{{
    """
    Add a user with a preconfigured home directory

    Add a user account with a skeleton directory structure
    from the config in the local skel dir
    """
    env.host_string = root_host

    run('useradd --skel '+remote_config_dir+'/skel --create-home --home-dir /home/'+user+' --shell /bin/bash '+user)
    run('yes "'+passw+'" | passwd ' + user)

# }}}
def add_prompt_to_user(home='/root', user='root'): # {{{
    """
    Add an awesomely cool shell prompt for a user 

    Our setup comes with a cool prompt but that comes from the
    skeleton directory for new users. If we are already a user, e.g.
    if we're root or the default system user then we've already got
    a home directory and some config files, so we'll need to
    gracefully add our setup with as little invasiveness as possible.

    The ``home`` and ``user`` parameters are used if you are making
    this copy as another user, for example as root. In that case,
    after you are done copying these files, you'll want to hand
    ownership over to the user in question, also you'll want
    the files to be uploaded to the proper home directory.
    """
    env.host_string = root_host

    put(local_config_dir+'/skel/.colors_prompts', home)
    put(local_config_dir+'/skel/.bash_prompt', home)
    put(local_config_dir+'/skel/.gemrc', home)
    with settings(hide('warnings'), warn_only=True):
        if run('[ ! -e '+home+'/.bashrc.bak ]').succeeded:
            run('cp '+home+'/.bashrc '+home+'/.bashrc.bak')
            run('echo >> '+home+'/.bashrc')
            run("echo 'if [ -f "+home+"/.colors_prompts ]; then . "+home+"/.colors_prompts; fi' >> "+home+"/.bashrc")
            run("echo 'if [ -f "+home+"/.bash_prompt ]; then . "+home+"/.bash_prompt; fi' >> "+home+"/.bashrc")

    # in other words if this was done as root
    if home != '~' and len(user) > 0:
        run('chown -R '+user+'.'+user+' '+home)

def select_prompt(name='remote_root', host=root_host):
    """
    Change the ~/.bash_prompt var to use the special red root prompt

    There are currently two prompts to select from, one is a regular
    user prompt that is green and red, and the other is the same
    but the all red to alter you that you are running commands as
    actual root and as so, to be careful.
    """
    env.host_string = host

    # choose the root prompt instead of the user prompt
    run("echo 'export PS1=$"+name+"' > ~/.bash_prompt")

# }}}
def backup_user_home(user): # {{{
    """
    Backup a users home dir to the backup dir

    If no backup yet exists for the given user's home directory
    then create a backup for that user in remote_backup_dir/home_user.tar.gz
    """
    env.host_string = root_host

    bak_file = remote_backup_dir+'/home_'+user+'.tar.gz'
    with settings(hide('warnings'), warn_only=True):
        if run('[ ! -e '+bak_file+' ]').succeeded:
            if run('[ -e /home/'+user+' ]').succeeded:
                with cd('/home'):
                    run('tar -czf '+bak_file+' '+user)

# }}}
def restore_user_home(user): # {{{
    """
    Restore a user's original home directory from the backup dir

    If a backup exists for the user's home directory, delete the
    current home directory and restore from the backup.
    """
    env.host_string = root_host

    bak_file = remote_backup_dir+'/home_'+user+'.tar.gz'
    with settings(hide('warnings'), warn_only=True):
        if run('[ -e '+bak_file+' ]').succeeded:
            if run('[ -e /home/'+user+' ]').succeeded:
                with cd('/home'):
                    run('rm -rf '+user)
                    run('tar -xzf '+bak_file)

# }}}
def reskel_existing_user(user, home=''): # {{{
    """
    Add custom user configuration to an existing user

    Backup the user's home directory and install
    fresh files from the custom skeleton instead
    """
    env.host_string = root_host

    if not len(home):
        home = '/home/'+user

    backup_user_home(user)

    # may want to add an option to override this
    # so hydration is non destructive
    run('rm -rf '+home)
    run('mkdir '+home)

    filenames = local('find skel -type f', capture=True).split('\n')
    for f in filenames:
        put(f, home)

    run('chown -R '+user+'.'+user+' '+home)
# }}}
