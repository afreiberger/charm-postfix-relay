import os
import sys
sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import host, hookenv


SERVICE = 'postfix'


def start_postfix():
    hookenv.status_set("active", "(re)starting {}".format(SERVICE))
    host.service_restart(SERVICE) or host.service_start(SERVICE)
    hookenv.status_set("active", "running")


def stop_postfix():
    hookenv.status_set("blocked", "stopping {}".format(SERVICE))
    host.service_stop(SERVICE)
    hookenv.status_set("blocked", "{} stopped".format(SERVICE))
