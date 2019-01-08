# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
from base64 import b64decode
from collections import OrderedDict
from jinja2 import Template
import os
import subprocess
import yaml

from charmhelpers.core.host import (
    install_ca_cert,
    service_restart,
    write_file,
)
from charmhelpers.core.hookenv import config


TEMPLATES = 'templates/'
MAIN_CFG = '/etc/postfix/main.cf'
AUTH_CONFIG = '/etc/postfix/sasl_passwd'
POSTFIX_CERTIFICATE_DIR = '/etc/postfix/'


def write_configs():
    cfg_template_path = os.path.join(TEMPLATES, 'main.cf')
    with open(cfg_template_path) as t:
        cfg_template = Template(t.read())
    with open(MAIN_CFG, 'w+') as f:
        f.write(cfg_template.render(PostfixContext()()))
    if config('smtp_auth_username') and config('smtp_auth_password'):
        write_auth_file()
    if config('domain_rewrite_map'):
        # create domain rewriting rules
        filename = '/etc/postfix/smtp_generic_maps.pcre'
        create_rewrite_map(config["domain_rewrite_map"], filename)
    restart_postfix()


def write_auth_file():
    auth_template_path = os.path.join(TEMPLATES, 'sasl_passwd')
    with open(auth_template_path) as t:
        auth_template = Template(t.read())
    with open(AUTH_CONFIG, 'w+') as f:
        f.write(auth_template.render(PostfixContext()()))
    os.chmod(AUTH_CONFIG, 0o600)
    subprocess.check_call(['postmap', 'hash:{}'.format(AUTH_CONFIG)])


def generate_rewrite(rewrites):
    """Produce a pcre-compatible rewrite entry for the domains in the supplied
    rewrite dictionary.  https://tools.ietf.org/html/rfc5322#section-3.2.3
    allows a much wider range than we do..."""
    if rewrites is not None:
        for domain, newdomain in rewrites:
            yield '/^([a-z0-9-_.]+)@([a-z][a-z0-9-_]+).' + domain + \
                '$/  $1+$2@' + newdomain + '\n'


def create_rewrite_map(rewrite, filename):
    """Save the rewrite dictionary to the supplied file."""
    f = open(filename, 'w')
    f.writelines(generate_rewrite(yaml.load(rewrite)))
    f.close()


def restart_postfix():
    service_restart('postfix')


def setup_ssl():
    ca = config('ssl_ca')
    install_ca_cert(b64decode(ca))


class PostfixContext():

    def __call__(self):
        ctxt =  {}
        ctxt['config'] = config()
        if config('ssl_ca'):
            ctxt['enable_ssl'] = True
        if config('domain_rewrite_map'):
            ctxt['have_rewrite_maps'] = True
        else:
            ctxt['have_rewrite_maps'] = False
        if config('smtp_auth_username') and config('smtp_auth_password'):
            ctxt['enable_auth'] = True
        if config('smtpd_helo_required'):
            ctxt['smtpd_helo_required'] = 'yes'
        else:
            ctxt['smtpd_helo_required'] = 'no'
        if config('disable_vrfy_command'):
            ctxt['disable_vrfy_command'] = 'yes'
        else:
            ctxt['disable_vrfy_command'] = 'no'
        return ctxt
