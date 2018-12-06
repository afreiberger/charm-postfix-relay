# Overview

This Postfix charm implements a naive mail relay for cloud instances.  It is
expected that it will be used as a simple transport to a more intelligent
upstream relay.

This is a reactive rewrite of ~paulgear/trusty/postfix-relay-0 which is based
on the postfix charm by:
 - Menno Smits <menno.smits@canonical.com>
 - Frank Mueller <frank.mueller@canonical.com>
 - Horacio Duran <horacio.duran@canonical.com>
 - John Weldon <johnweldon4@gmail.com>


# Maintainers

Canonical IS <root@admin.canonical.com>


# TODO

- Provide juju actions to
  - add/remove/list postconf entries?
  - add/remove/list aliases
  - remove/list entries in the mail queue?
