#!/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os
import sys
import crypt


def environnement_to_list(environnement_var, reference_size=None,
        reference_var='AUTOCLEANFTP_USERS'):
    res = [x.strip()
           for x in os.environ.get(environnement_var, '').split(',')]
    if len(res) == 1 and len(res[0]) == 0:
        res = []
    if reference_size is not None:
        if len(res) != reference_size:
            print("%s environnement variable and %s one don't have the same "
                  "number of elements (separated by comma) => exiting",
                  (environnement_var, reference_var), file=sys.stderr)
            sys.exit(1)
    return res



users = environnement_to_list('AUTOCLEANFTP_USERS')
length = len(users)

passwords = environnement_to_list('AUTOCLEANFTP_PASSWORDS',
        reference_size=length)
uids = environnement_to_list('AUTOCLEANFTP_UIDS', reference_size=length)
lifetimes = environnement_to_list('AUTOCLEANFTP_LIFETIMES',
        reference_size=length)

gid = os.environ.get('AUTOCLEANFTP_GID', '')

# users and passwords in /etc/shadow are stored in a dictionary
# passwd['user'] = 'password'
with open('/etc/shadow', 'r') as passfile:
    passwd = {}
    for line in passfile.readlines():
        line = line.replace("\n","").split(":")
        if  line[1] != '*' and line[1].startswith('$6'):
            passwd[line[0]] = line[1]

for i, user in enumerate(users):
    password = passwords[i]
    uid = uids[i]
    lifetime = int(lifetimes[i])
    command0 = '/usr/sbin/groupadd --force --gid=%s ftpusers' % (gid,)
    command1 = 'mkdir -p "/data/%s"' % user
    command2 = '/usr/sbin/useradd --no-create-home --home-dir="/data/%s" ' \
               '--no-user-group --non-unique --gid=%s --shell=/sbin/nologin ' \
               '--uid=%s "%s"' % (user, gid, uid, user)
    command3 = 'chown -R "%s:ftpusers" "/data/%s"' % (user, user)
    command4 = 'echo "%s" |passwd "%s" --stdin >/dev/null' % (password, user)
    os.system(command0)
    os.system(command1)
    if not passwd.has_key(user):
        # New users (only the new ones) are created with passwords
        if os.system(command2) == 0:
            print("User created %s (%s, %s)..." % (user, uid, gid))
        os.system(command4)
    else:
        # Passwords for existing users are changed (only if they really changed)
        insalt = "$6$" + passwd[user].split("$")[2] + "$"
        if passwd[user] != crypt.crypt(password, insalt):
            if os.system(command4) == 0:
                print("Password changed for user %s" % user)
    os.system(command3)
    if lifetime > 0:
        if lifetime < 10:
            when = "* * * * *"
        elif lifetime < 50:
            when = "*/5 * * * *"
        elif lifetime < 14400:
            when = "0 * * * *"
        else:
            when = "0 0 * * *"
        with open("/etc/cron.d/autoclean_vsftpd_%s" % user, "w") as f:
            f.write("%s root find /data/%s -type f -mmin +%i -exec rm -Rvf {} \; "
                    ">/dev/null 2>&1\n" % (when, user, lifetime))
