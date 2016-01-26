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

The first choice is _ejabberd_, which is also available in the repository of Ubuntu but only in a quite old version. The documentation found is only valid for never versions, which changed a lot (e.g. configuration file format changed from erlang to yaml). So my choice is to try the latest, well documented version. Luckily there is a debian file and also an installer available. The latest version 16.01, after successful installation, always produces an error when the service is stopped. Switching back to a lower version 15.11 does not produce that error anymore. Only thing left to do is to copy the already delivered init script to `/etc/init.d`, to be able to control the service easily with puppet.

A second server software is _prosody_, which is claimed to be efficient and easy to use. As this one is available via the package repository, I will try to use it as well. It comes with a minor flaw: The init script of prosody does not provide the status of the service. Puppet can handle that, but for the service statement it is necessary to provide `hasstatus=False`, to control the service with Puppet.

_ejabber_ comes with a build in clustering feature that helps scaling the application and/or make it more fault tolerant.
You can find a diagram here: http://docs.ejabberd.im/architect/

I will try both.

###Setup

I decided to just use a simple setup:

1 server with prosody and mysql installation 
1 server with ejabberd using internal storage

optional:
1 server with haproxy as loadbalancer for several ejabberd instance
1 server with ejabberd for clustering

The storage method can be changed according to the needs. I decided to use mysql for prosody just to use something different than the internal storage for this example. 

