=====
Tasks
=====

.. _tasks-overview:

Tasks Overview
==============

Tasks  have a  few basic  naming conventions  based on  what
their names start with.

* ``setup_*``   These are compound tasks that call other tasks
* ``install_*`` These are where all the work is done for the most part
* ``aptget_*``  Software installation from the package manager, ubuntu specific
* ``clean_*``   Deletes some sort of config or automatically generated file
* ``restore_*`` Restores some part of the system to its original pristine state
* ``backup_*``  Backs up some files prior editing part of the system's configuration
* ``regen_*``   Local config file generation and packaging
* ``test_*``    Really simple tests for validating that your connections work

There are  a handful  of other  slightly less  standard task
names,  most of  which  are  meant to  be  utility tasks  of
some  kind or  aren't  as modular  and  repeatable as  these
other  standard tasks  and so  don't necessarily  follow any
particular naming conventions.

Most  of  the  tasks  are  fairly  module  and  specifically
suited  to being  put  together to  form more  comprehensive
administration tasks that are common enough to be cumbersome
on their own and when modularized, allow new more powerfully
expressive ways of getting stuff done.

I highly encourage you to try running single tasks at a time
and watching what they do on the server.

.. _customizing-tasks:

Venturing Outside The Box
=========================

If you want to do  anything more complicated than the config
files will allow,  then you'll want to modify  the fab tasks
themselves.

To  get an  idea  of  how to  modify  these  tasks, I  would
recommend  reading the  Task API  and then  also looking  at
:doc:`config_dir`

If  you want  to  for  example change  the  way gitolite  or
Apache adds  users and  vhosts, you'll want  to look  at the
``install_`` related tasks

You  may  likely  also  want  to change  the  way  that  the
``regen_``  tasks  work because  these  are  the tasks  that
actually put  together your config  files for upload  to the
server

Any  ``install_`` related  task you  create should  probably
have a  corresponding ``backup_`` and ``restore_``  task, or
at the very  least a ``clean_`` task, but none  of these are
strictly necessary.

If  you want  to  adapt this  for  a different  distribution
you'll want to look at the ``aptget_`` related tasks and add
corresponding tasks for ``yum``

.. _task-api:

Task API
==========================

Here is the documentation for each fab task that is available

You can of course, also see this list with ``fab --list``

.. automodule:: quickfab.ubuntu.fabfile
    :members:
