Documentation Erasys Test Task
==============================

Realtime Messaging Infrastructure
---------------------------------

Task:

*Provide a manifest for a configuration management tool of your choice that automatically provisions a Virtualbox based VM, automatically installs a chat server and all required dependencies
write a simple CLI
choose your favourite language for this task
don't reinvent the wheel: use a library or wrap existing clients
comply to POSIX standard "Utility Argument Syntax"*

Implement these commands:
- show unread messages for a given user
- send a message to a given user*


First step:

Gather some information about chat servers and requirements


I'm going to use Vagrant and Virtualbox building machines with Ubuntu 14.04 (trusty) as operating system, puppet as configuration tool.

To use the benefits of Ubuntu's packaging system I will look for chat server solutions that offer debian packages, ideally with there own package repository or with not too old versions already included into the OS's repository.

My first choice for a chat server software is jabberd2, as it is available in Ubuntu's software repository. However, it seems there is a problem when using puppet to handle the jabberd2 service. Puppet uses upstart as start/ stop provider, but the jabberd2 package does not seem to implement upstart the correct way.
Installation of the package does work without any problems, but the service just can't be managed from within puppet without changing or even creating more scripts. To avoid further problems, I decided to not use jabberd2 for this task.

The second choice is ejabberd. It is also available in the repository of Ubuntu but only in a quite old version. The documentation found is only valid for never versions, which changed a lot (e.g. configuration file format changed from erlang to yaml). So my choice is to try the latest, well documented version. Luckily there is a debian file and also an installer available.

So, after trying out jabberd2, I decided to just switch to another solution: ejabberd. Here the service management from puppet works just like expected.

I also chose MySQL as a persistent data storage as it is a quite common database solution.
