#!/usr/bin/env python

import sys
import logging
import getpass
import argparse

import sleekxmpp


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class SendMsg(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message, show_messages):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message
        self.show_messages = show_messages

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        if self.show_messages is False:
            self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')

    def message(self, msg):
        print(str(msg))
        if msg['type'] in ('chat', 'normal'):
            print("Message: " + str(msg['body']) + "\nsent from " + str(msg['from']))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--show_messages', help='only show messages', action='store_const', dest='show_messages', const=True, default=False)
    parser.add_argument('-d', '--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-v', '--verbose', help='set logging to VERBOSE', action='store_const', dest='loglevel', const=5, default=logging.INFO)

    parser.add_argument("-j", "--jid", dest="jid", help="JID to use")
    parser.add_argument("-p", "--password", dest="password", help="password to use")
    parser.add_argument("-t", "--to", dest="to", help="JID to send message to")
    parser.add_argument("-m", "--message", dest="message", help="message to send")

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = raw_input("Username: ")
    if args.password is None:
        args.password = getpass.getpass("Password: ")
    if args.show_messages is False:
        if args.to is None:
            args.to = raw_input("Send To: ")
        if args.message is None:
            args.message = raw_input("Message: ")

    xmpp = SendMsg(args.jid, args.password, args.to, args.message, args.show_messages)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0199')

    if xmpp.connect(('myejabberd', 5222)):

        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect")
