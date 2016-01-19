from __future__ import print_function
import os
import sys


def environnement_to_list(environnement_var, reference_size=None,
        reference_var='AUTOCLEANFTP_USERS'):
    res = [x.strip()
           for x in os.environ.get(environnement_var, '').split(',')]
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
gids = environnement_to_list('AUTOCLEANFTP_GIDS', reference_size=length)
lifetimes = environnement_to_list('AUTOCLEANFTP_LIFETIMES',
        reference_size=length)

for i, user in enumerate(users):
    password = passwords[i]
    uid = uids[i]
    gid = gids[i]
    lifetime = int(lifetimes[i])
    print("Creating user %s (%s, %s)..." % (user, uid, gid))
    command0 = '/usr/sbin/groupadd --force --gid=%s ftpusers' % (gid,)
    command1 = 'mkdir -p "/home/%s"' % user
    command2 = '/usr/sbin/useradd --no-create-home --home-dir="/home/%s" --no-user-group --non-unique --gid=%s --shell=/sbin/nologin --uid=%s "%s"' % (user, gid, uid, user)
    command3 = 'chown -R "%s:ftpusers" "/home/%s"' % (user, user)
    command4 = 'echo "%s" |passwd "%s" --stdin >/dev/null' % (password, user)
    os.system(command0)
    os.system(command1)
    os.system(command2)
    os.system(command3)
    os.system(command4)
    if lifetime > 0:
        if lifetime < 100:
            when = "* * * * *"
        elif lifetime < 500:
            when = "*/5 * * * *"
        elif lifetime < 14400:
            when = "0 * * * *"
        else:
            when = "0 0 * * *"
        with open("/etc/cron.d/autoclean_vsftpd", "w") as f:
            f.write("%s find /home/%s -type f -mmin +%i -exec rm -Rvf {} \; 2>&1 |logger -t autoclean\n" % (when, user, lifetime))