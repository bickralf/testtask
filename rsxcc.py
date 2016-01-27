#!/usr/bin/env python

import sys
import logging
import getpass
import argparse

import sleekxmpp

"""
    Author: Ralf Bickel - ralf.bickel@googlemail.com

    Using SleekXMPP: The Sleek XMPP Library
    Copyright (c) 2010 Nathanael C. Fritz

    http://sleekxmpp.com/
    Find source code at https://github.com/fritzy/SleekXMPP

    rsxcc.py  -  ridiculously simple xmpp chat client

    With this simple script you can send a message to a give jid or you can get unread messages for a jid and print them to the console.
"""


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class SimpleChatClient(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message_content, show_unread_messages, continuous):
        """
        Arguments:
            jid - Jabber ID to use
            password - Password that belongs to the jid
            recipient - Jabber ID of recipient
            message_content - message content
            show_unread_messages - if set only shows unread messages of jid
            continuous - if set program runs continuously
        """

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        # Set message content and recipient.
        self.recipient = recipient
        self.msg_content = message_content
        # Set switches
        self.show_unread_messages = show_unread_messages
        self.continuous = continuous

        # Register event handler
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Send initial presence stanza and get the roster. Send Message if
        show_unread_messages is not set. Disconnect after Message was sent unless
        continuous is set.
        """
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.jid, mbody="No more unread Messages\n", mtype='chat')
        if self.show_unread_messages is False:
            self.send_message(mto=self.recipient, mbody=self.msg_content, mtype='chat')
            if self.continuous is False:
                self.disconnect(wait=True)

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

if __name__ == '__main__':
    # Set up the command line arguments.
    parser = argparse.ArgumentParser()

    parser.add_argument("-j", "--jid", dest="jid", help="JID to use (username@example)", required=True)
    parser.add_argument("-p", "--password", dest="password", help="Password to use")
    parser.add_argument("-x", "--xmpp_host", dest="xmpp_host", help="Set the xmpp host to use")
    parser.add_argument("-t", "--to", dest="to", help="JID to send message to")
    parser.add_argument("-m", "--message", dest="message", help="The message content")

    parser.add_argument('-d', '--debug', help='Set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.ERROR)
    parser.add_argument('-v', '--verbose', help='Set logging to VERBOSE', action='store_const', dest='loglevel', const=5, default=logging.ERROR)
    parser.add_argument('-s', '--show_unread_messages', help='Only show unread messages than log out', action='store_const', dest='show_unread_messages', const=True, default=False)
    parser.add_argument("-c", "--continuous", help="Set if program should run until you close it with control-c", action='store_const', dest="continuous", const=True, default=False)

    args = parser.parse_args()

    # Set up logging according to the arguments.
    if args.loglevel == 'logging.DEBUG' or 5:
        logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')

    # If the required arguments are not set, ask for them via input.
    if args.jid is None:
        args.jid = raw_input("Username: ")
    if args.password is None:
        args.password = getpass.getpass("Password: ")
    if args.show_unread_messages is False:
        if args.to is None:
            args.to = raw_input("Send To: ")
        if args.message is None:
            args.message = raw_input("Message: ")

    xmpp = SimpleChatClient(args.jid, args.password, args.to, args.message, args.show_unread_messages, args.continuous)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    if args.xmpp_host is None:
        # Tries to connect with the server specified in the jid if no host is specified via the xmpp_host argument
        if xmpp.connect():
            xmpp.process(block=True)
            print("Done")
        else:
            print("Unable to connect")
    else:
        if xmpp.connect((args.xmpp_host, 5222)):
            xmpp.process(block=True)
            print("Done")
        else:
            print("Unable to connect")
