# These settings are listed in what I believe to be an order
# that reflects the settings most likely to change.
# Full documentation in docs/settings.html

# You should at least provide a hostname in FQDN format!
#################################################################
server_hostname  = ''

# You probably also want to change these settings
#################################################################
main_username    = 'masterchief' # this is the sudo user

main_password    = 'admin1234'
deploy_password  = 'webmaster1234'
team_password    = 'dev1234'

team_users       = [ 'mary', 'john' ]
git_repo_devteam = [ 'mary', 'john', 'bill', 'ted' ]
git_hosted_repos = [ 'someproject', 'clientdemo', 'superblog' ]

# You can probably leave the rest of these settings alone
#################################################################
single_user_mode = False

# Hostname setting is required (don't touch this)
#################################################################
# original panic mode
#import sys
#if not len(server_hostname) and len(server_domain)):
#    sys.exit()

# graceful mode
from fabric.api import *
if not (len(server_hostname) and len(server_domain)):
    print """
        It  looks like  this is  the first  time
        you've run this  program. To get started
        you'll  need root access and a  hostname

        Your hostname must be in FQDN format.

        To make this message go away:
            * Put your hostname in settings.py

    """

    server_hostname = prompt(
        'What is your hostname?', 
        default='thundercloud.mycorp.dyndns.org',
        validate=r'^([-a-zA-Z_]+?\.)+([-a-zA-Z_]+)$')
    server_domain = server_hostname.partition('.')[2]
    server_fqdn   = server_hostname
else:
    if not len(server_domain):
        server_domain = server_hostname.partition('.')[2]
        server_fqdn   = server_hostname
    else:
        server_fqdn = server_hostname+'.'+server_domain

# You can probably leave the rest of these settings alone
#################################################################
team_groupname   = 'developers'
deploy_username  = 'webmaster'

git_repo_devteam.append(deploy_username)
if not single_user_mode:
    git_repo_devteam.append(main_username)
    git_repo_admins = [ main_username ]
else:
    git_repo_admins = [ deploy_username ]

gitolite_admin_local = '~/etc/gitolite/'+server_hostname
gitolite_admin_name  = 'Repository Manager'
gitolite_admin_email = 'gitolite@'+server_fqdn
gitolite_admin_user  = main_username

team_sudo_cmds = [
    "/usr/sbin/a2ensite",
    "/usr/sbin/a2dissite",
    "/usr/sbin/a2enmod",
    "/usr/sbin/a2dismod",
    "/usr/sbin/service nginx start",
    "/usr/sbin/service nginx stop",
    "/usr/sbin/service nginx restart",
    "/usr/sbin/service apache2 restart",
    "/usr/sbin/service apache2 reload",
    "/usr/sbin/service apache2 start",
    "/usr/sbin/service apache2 stop"
]

local_config_dir  = './conf'
remote_backup_dir = '/var/dumps/maverick_cloud_fabfile'
remote_config_dir = '/var/local/maverick_cloud_fabfile'

server_groupname       = 'www-data'

webroot_dir            = '/var/www'
python_environment_dir = '~/Envs'

vim_config_tarball_url = 'http://rocksolidwebdesign.com/pub/vim/cloud_vim.tar.bz2'
