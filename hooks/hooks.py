#!/usr/bin/env python

import sys
import common  # mangle sys.path

from charmhelpers.core import hookenv

hooks = hookenv.Hooks()
log = hookenv.log


def main(argv):
    log('postfix {}'.format(argv[0]))


if __name__ == "__main__":
    main(sys.argv)
