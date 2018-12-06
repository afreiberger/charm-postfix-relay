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

from charmhelpers.core.host import (
    install_ca_cert,
    service_restart,
    write_file,
)

from charm.postfix.postfix_relay_context import PostfixContext


TEMPLATES = 'templates/'
MAIN_CFG = '/etc/postfix/main.cf'
POSTFIX_CERTIFICATE_DIR = '/etc/postfix/'


def write_configs():
    template_path = os.path.join(TEMPLATES, 'main.cf')
    with open(template_path) as t:
        template = Template(t.read())
    with open(MAIN_CFG, 'w+') as f:
        f.write(template.render())


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
        return ctxt
