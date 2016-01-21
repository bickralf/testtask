Documentation Erasys Test Task
==============================

Realtime Messaging Infrastructure
---------------------------------

Task:

Provide a manifest for a configuration management tool of your choice that automatically provisions a Virtualbox based VM, automatically installs a chat server and all required dependencies
write a simple CLI
choose your favourite language for this task
don't reinvent the wheel: use a library or wrap existing clients
comply to POSIX standard "Utility Argument Syntax"

Implement these commands:
- show unread messages for a given user
- send a message to a given user



I am going to use puppet as the configuration management tool of choice.

My first choice for a chat server software was jabberd2, however, it seems there is a problem when using puppet to handle the jabberd2 service. Puppet uses upstart as start/ stop provider, but the jabberd2 package does not seem to implement upstart the correct way.
Installation of the package does work without any problems, but the service just can't be managed from within puppet.

So, after trying out jabberd2, I decided to just switch to another solution: ejabberd. Here the service management from puppet works just like expected.

I also chose MySQL as a persistent data storage as it is a quite common database solution.
