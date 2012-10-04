#!/usr/bin/env python
import argparse
import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

ADMIN_TYPE = 2

def main():
    parser = argparse.ArgumentParser()
    cmdparsers = parser.add_subparsers(dest="command")
    # launch
    launch_parser = cmdparsers.add_parser('launch')
    launch_parser.add_argument('-i', '--ipaddr', help='bind instance to ip')
    launch_parser.add_argument('-p', '--port', help='bind instance to port')
    # create admin
    admin_parser = cmdparsers.add_parser('createadmin')
    # create module
    module_parser = cmdparsers.add_parser('createmodule')
    module_parser.add_argument('-n', '--name', help='module name to create')

    args = parser.parse_args()

    cmd = globals()[args.command]
    cmd(args)


def createmodule(args):
    # Create module directory structure
    print "Create the module",
    if args.name:
        print args.name

def createadmin(args):
    from app import settings
    from hashlib import md5

    if settings.connection.User.find_one({'usertype':ADMIN_TYPE}):
        print "An administrator already exists in the database."; return

    email = raw_input("Enter the e-mail address: ")
    pass1 = raw_input("Enter the password: ")
    pass2 = raw_input("Confirm password: ")
    if pass1 != pass2:
        print "Passwords do not match"; return

    admin_user = settings.connection.User()
    admin_user.usertype = ADMIN_TYPE
    admin_user.set_password(pass1)
    admin_user.name = u'Administrator'
    admin_user.email = unicode(email)
    admin_user.save()
    print "Administrator user created : %s" % (email)


def launch(args):
    from app import tornapp

    if args.port:
        tornapp.settings['instance_port'] = int(args.port)

    if args.ipaddr:
        tornapp.settings['instance_ipv4'] = str(args.ipaddr)

    print "Launching Tornado %s:%s" % (
        tornapp.settings['instance_ipv4'],
        tornapp.settings['instance_port']
        )

    start_instance(tornapp)


def start_instance(application):
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(
        application.settings.get('instance_port'),
        address=application.settings.get('instance_ipv4')
        )

    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


if __name__ == "__main__":
    main()
