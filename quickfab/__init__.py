# Main Settings

# the main user setup concept here is based on the following:
#   - one root account
#
#   - one master user account with full sudo privileges
#     essentially a root equivalent
#
#   - one deploy user account that can edit all website files
#     and who can restart the webserver without a password
#
#   - a number of web developers who will want access to
#     the server and who will also want shell account
#     these users will also have similarly limited
#     privileges, even further limited in their abilities
#     to muck about with other people's files
#
# if you are never going to really have any other users except root
# and the web server user, then choose single_user_mode = True
#
# this will result in only a single extra user, the deploy user
# being created. The deploy user will own and have full access to
# the webroot and vhost config directories and the deploy user 
# will have full sudo privileges.
single_user_mode = False

# SERVER
# the root directory for served file to the web
# this directory will be backed up if it exists
# and created if it does not exist
webroot_dir            = '/var/www'

# the hostname of the server you'll actually be running
server_domain    = 'myserver.dyndns.org'
server_hostname  = 'thundercloud'
server_groupname = 'www-data'

# USERS
# the name of the directory where each user will
# store their virtualenvironments
python_environment_dir = '~/Envs'

# this is your main username - you, the person who will
# be running this fabfile. so for example 'john' or 'mary'
# 'superhacker', 'mrcool' or whatever username you want.
#
# if you'r installing via sudo this should be the username
# of the user who has those sudo privileges. for example
# if you're installing to a virtual machine
main_username    = 'jerry'
main_password    = 'jerry1234'

# the deploy user is your "everything web" user. your
# deploy user will own all the files that belong to
# your actual websites, your deploy user will be
# able to restart the web server and add vhosts
# without requiring a password
deploy_username  = 'webmaster'
deploy_password  = 'webmaster1234'

# if you have a list of other users, probably
# developers who will need shell accounts then 
team_groupname   = 'developers'
team_password    = 'dev1234'
team_users       = [ 'mary', 'john', 'martha', 'jennifer' ]

# GIT
# You will need to checkout the gitolite admin repo
# on to your local computer to add the keys for the deploy
# user so that the deploy user can checkout your projects
# in to your various webroot folders
gitolite_admin_local_dir = '~/etc/gitolite/'+server_hostname
gitolite_admin_user = 'Billy Badger'
gitolite_admin_email = 'gobadgers@billyb.com'

# usernames of the users who are actually allowed to admin and
# maintain the repositories and who has access to them
git_repo_admins    = [ main_username ]

# these are your actual developers who will need commit 
# access to your repositories
git_repo_devteam   = [ 'mary', 'john', main_username, deploy_username ]

# this is your list of git repositories
git_hosted_repos   = [ 'someproject', 'pastebin', 'clientdemo', 'superblog' ]

# These are the commands your deploy user can run, basically
# to allow restarting the web server and other common web
# server related tasks
team_sudo_cmds   = [
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

# These are the commands your deploy user can run, basically
# to allow restarting the web server and other common web
# server related tasks. You should choose a directory
# that does not yet exist for these settings.
backup_dir = '/var/dumps/ubuntucloud_fabfile'
config_dir = '/var/local/ubuntucloud_fabfile'

# If you want a custom vim configuration you can use this one
# If you want your own just point this to the URL of a tarball
# that contains simply a .vim folder and .vimrc file
vim_config_tarball = 'http://rocksolidwebdesign.com/pub/vim/cloud_vim.tar.bz2'
