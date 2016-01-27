Documentation Erasys Test Task
==============================


Realtime Messaging Infrastructure
---------------------------------

###Task

*Provide a manifest for a configuration management tool of your choice that automatically provisions a Virtualbox based VM, automatically installs a chat server and all required dependencies
write a simple CLI
choose your favourite language for this task
don't reinvent the wheel: use a library or wrap existing clients
comply to POSIX standard "Utility Argument Syntax"*

Implement these commands:
- show unread messages for a given user
- send a message to a given user*


###First step

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

    1 server with prosody and mysql installation for storage

and a bit more complex setup for ejabberd:

    1 server with haproxy as loadbalancer for the ejabberd cluster servers and a dns server
    2 servers with ejabberd using internal storage in a cluster

As ejabberd brings it own clustering functionality that works best with it's internal storage solution (based on mnesia), I stick to that in this example.

I use haproxy for loadbalancing between the two servers in the ejabberd clusters to have one "interface". So if I want to connect to the servers I can just use one address, the address from the loadbalancer. The load is balanced equally on the two servers. With the clustering feature both servers communicate with each other via s2s (server-to-server) and exchange data.

###Directory structure:

```
root
|
+-- Vagrantfile          - the Vagrantfile containing definitions for all 4 servers
    +-- documentation.md     - this documentation
    +-- ejabberd             
        |
        +-- files             - all files used for provisioning ejabberd, especially config files
        +-- manifests         - a single puppet manifest for provisioning ejabberd
    +-- ejabberd_slave
        |
        +-- files             - all files used for provisioning ejabberd slave, especially config files
        +-- manifests         - a single puppet manifest for provisioning ejabberd slave
    +-- haproxy
        |
        +-- files             - all files used for provisioning haproxy, especially config files
        +-- manifests         - a single puppet manifest for provisioning haproxy
    +-- prosody
        |
        +-- files             - all files used for provisioning prosody, especially config files
        +-- manifests         - a single puppet manifest for provisioning prosody
    +-- scripts
        |
        +-- chat_task.py      - python script to send messages and show unread messages
   ```

The vagrant machines are named according to the directory names:
```
- ejabberd
- ejabberd_slave
- haproxy
- prosody
```

###Getting started

It is important to start the ejabberd before the ejabberd_slave, as the erlang cookie needs to be copied from ejabberd to ejabberd_slave!

Example command to start a machine
`vagrant up haproxy`

The puppet manifests are all called `site.pp` and can be found in the respective directories.

For this example I used simple puppet manifests. For a production environment I would set up a puppet master and install puppet agents on the 4 servers. This has the advantage, that puppet can run periodically, and therefore can make sure that services run or restart them. With a puppet master/agent approach it would also make sense to use the module structures of puppet to be able to reuse modules. Tools like Hiera and librarian/r10k should be helpful in such a scenario.

https://github.com/rodjek/librarian-puppet

https://github.com/puppetlabs/r10k

https://docs.puppetlabs.com/hiera/latest/

After machines are started, you can log in via
`vagrant ssh <machine name> e.g. vagrant ssh ejabberd`

After all machines have been started you may either edit your hosts file or set your machine to use the installed dns server.

Here is an example for entries to a hosts file:

```
192.168.20.10 xmpp.myprosody myprosody xmpp.myprosody.chatexample.com myprosody.chatexample.com
192.168.20.20 xmpp.myejabberd1 myejabberd1 xmpp.myejabberd1.chatexample.com myejabberd1.chatexample.com
192.168.20.21 xmpp.myejabberd2 myejabberd2 xmpp.myejabberd2.chatexample.com myejabberd2.chatexample.com
192.168.20.100 xmpp.myejabberd xmpp.myejabberd.chatexample.com myejabberd myejabberd.chatexample.com
```

This enables you to easily access all servers from your host machine.

###Send and receive some messages
#### RSXCC - Ridicously simple xmpp chat client

You can now use the script `rsxcc.py`, it uses python 2.7 and you have to install sleekxmp to make it work.

I chose python, because it is good to write efficient scripts that are easy to understand. Sleekxmpp seems like a good library for xmpp, that is easy to set up and use. Unfortunately the documentation is not complete and to understand certain features and functions you will have to dig into the sources.

http://sleekxmpp.com/

You'll need `python-pip` to install it via

`pip install sleekxmpp`

You may also need to set PYTHONPATH to the path were all python modules are installed.

For Mac it is something like:

`export PYTHONPATH=/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages`

You can call the script with `<path-to-script>/rsxcc.py --help` to get all available arguments.

```
usage: rsxcc.py [-h] -j JID [-p PASSWORD] [-x XMPP_HOST] [-t TO]
                    [-m MESSAGE] [-d] [-v] [-s] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -j JID, --jid JID     JID to use (username@example)
  -p PASSWORD, --password PASSWORD
                        Password to use
  -x XMPP_HOST, --xmpp_host XMPP_HOST
                        Set the xmpp host to use
  -t TO, --to TO        JID to send message to
  -m MESSAGE, --message MESSAGE
                        The message content
  -d, --debug           Set logging to DEBUG
  -v, --verbose         Set logging to VERBOSE
  -s, --show_unread_messages
                        Only show unread messages than log out
  -c, --continuous      Set if program should run until you close it with
                        control-c
```

Example to send a message:

`/rsxcc.py -j bob@myejabberd.chatexample.com -p 12345 -x myejabberd.chatexample.com -t alice@myejabberd.chatexample.com -m 'Hi Alice'`

Example to show unread messages:

`./rsxcc.py -j alice@myejabberd.chatexample.com -p 12345 -x myejabberd.chatexample.com -s`

You don't have to specify an xmpp host, if your jid contains a valid host:

`./rsxcc.py -j alice@myejabberd.chatexample.com -p 12345 -s`


###Some more info

This example does not take care of security! With a production xmpp infrastructure, valid and signed certifactes as well as encrypted message transportation are vital. The mysql database would need to be secured with a password for the root account, better passwords would need to be chosen (12345 is used only for simplicity here) and should not appear plain in puppet manifests.

The DNS server (implemented with bind9) is necessary to get the ejabberd clustering to work. Alternatively dnsmasq can be used, but a dedicated DNS server seemed to be a better solution for me.

###Problems on the way

- The packages provided come with some flaws and can't always be used out of the box. It took some time to figure out why services could not be controlled or why errors occured with freshly installed packages.

- The cluster feature of ejabberd does not work "out-of-the-box" if DNS is not used and the server hostnames are not similar to the erlang node names. It needed a lot of investigation to get this to run but once it is clear, what needs to be archived the whole process of clustering ejabberd works smoothly.

- As sleekxmpp's documentation misses some entries, digging through the sources was necessary and took some time, to achieve the script's wanted functionality. Closing and disconnecting the application from the xmpp servers xml stream automatically, if there are no messages in the stream is a problem. The script shows unread messages and then quits. This works fine if there are any messages. But if there are no messages, the script either ran continuously or quit before messages could be fetched.

If there are no messages, the script would never get into the message method:
```
    def message(self, msg):
        """
        Process all unread message stanzas of given jid.
        Disconnects if continuous is not set, otherwise prints all messages
        as long as the program runs.
        """
        if msg['type'] in ('chat', 'normal'):
            if self.jid in str(msg['from']):
                print(str(msg['body']))
            else:
                print("Message: " + str(msg['body']) + "\nsent from " + str(msg['from']))
        if self.continuous is False:
            if self.event_queue.qsize() == 0:
                self.disconnect(wait=True)
```

Putting the `self.disconnect(wait=True)` either into the `start` or `init` method would prevent the script from printing out any unread messages.

This behaviour is due to the event based nature of sleekxmpp. I created a workaround, sending a message "No more unread Messages" to the user, so a message event is always fired and the script gets into the ´message´ method where it can then quit.

###Credits

Author: Ralf Bickel
ralf.bickel@googlemail.com
