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

The first choice is _ejabberd_ as it seems to be not only well documented, but has also a lot of features, is often used as xmpp server and is still actively developed. It is also available in the repository of Ubuntu but only in a quite old version. The documentation found is only valid for never versions, which changed a lot (e.g. configuration file format changed from erlang to yaml). So my choice is to try the latest, well documented version. Luckily there is a debian file and also an installer available. The latest version 16.01, after successful installation, always produces an error when the service is stopped. Switching back to a lower version 15.11 does not produce that error anymore. Only thing left to do is to copy the already delivered init script to `/etc/init.d`, to be able to control the service easily with puppet.

A second server software is _prosody_, which is claimed to be efficient and easy to use. It has a comprehensive documentation and many feaures. As this one is available via the package repository, I will try to use it as well. It comes with a minor flaw: The init script of prosody does not provide the status of the service. Puppet can handle that, but for the service statement it is necessary to provide `hasstatus=False`, to control the service with Puppet.

_ejabber_ comes with a build in clustering feature that helps scaling the application and/or make it more fault tolerant.
You can find a diagram here: http://docs.ejabberd.im/architect/

I will try both solutions to find out if my script can work with different servers.

###Setup

I decided to just use a simple setup for prosody:

*1 server with prosody and mysql installation for storage*

and a bit more complex setup for ejabberd:

1 server with haproxy as loadbalancer for the ejabberd cluster servers and a dns server
2 servers with ejabberd using internal storage in a cluster

As ejabberd brings it own clustering functionality that works best with it's internal storage solution (based on mnesia), I stick to that in this example.

Directory structure:

```
root
|
+-- Vagrantfile          - the Vagrantfile containing definitions for all 4 servers
    +-- documentation.md     - this documentation
    +-- ejabberd             
        |
        +-- files             - all files used for provisioning ejabberd
        +-- manifests         - a single puppet manifest for provisioning ejabberd
    +-- ejabberd_slave
        |
        +-- files             - all files used for provisioning ejabberd slave
        +-- manifests         - a single puppet manifest for provisioning ejabberd slave
    +-- haproxy
        |
        +-- files             - all files used for provisioning haproxy
        +-- manifests         - a single puppet manifest for provisioning haproxy
    +-- prosody
        |
        +-- files             - all files used for provisioning prosody
        +-- manifests         - a single puppet manifest for provisioning prosody
    +-- scripts
        |
        +-- chat_task.py      - python script to send messages and show unread messages
   ```

The vagrant machines are named according to the directory names:
````
- ejabberd
- ejabberd_slave
- haproxy
- prosody
```

It is important to start the ejabberd before the ejabberd_slave, as the erlang cookie needs to be copied from ejabberd to ejabberd_slave!

Example command to start a machine
`vagrant up haproxy`

The puppet manifests are all called `site.pp` and can be found in the respective directories.

For this example I used simple puppet manifests. For a production environment I would set up a puppet master and install puppet agents on the 4 servers. This has the advantage, that puppet can run periodically, and therefore can make sure that services run or restart them. With a puppet master/agent approach it would also make sense to use the module structures of puppet to be able to reuse modules. Tools like Hiera and librarian/r10k should be helpful in such a scenario.

https://github.com/rodjek/librarian-puppet
https://github.com/puppetlabs/r10k
https://docs.puppetlabs.com/hiera/latest/

After machines are started, you can log in via
`vagrant ssh <machine name> e.g. ejabberd``

After all machines have been started you may either edit your hosts file or set your machine to use the installed dns server.

Here is an example for entries to a hosts file:

```
192.168.20.10 xmpp.myprosody myprosody xmpp.myprosody.chatexample.com myprosody.chatexample.com
192.168.20.20 xmpp.myejabberd1 myejabberd1 xmpp.myejabberd1.chatexample.com myejabberd1.chatexample.com
192.168.20.21 xmpp.myejabberd2 myejabberd2 xmpp.myejabberd2.chatexample.com myejabberd2.chatexample.com
192.168.20.100 xmpp.myejabberd xmpp.myejabberd.chatexample.com myejabberd myejabberd.chatexample.com
```

This enables you to easily access all servers from your host machine.

You can now use the script, it uses python 2.7 and you have to install sleekxmp to make it work.

http://sleekxmpp.com/

You'll need `python-pip` to install it via

`pip install sleekxmpp``

You may also need to set PYTHONPATH to the path were all python modules are installed.

For Mac it is something like:

`export PYTHONPATH=/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages`

Depending on your setup.

