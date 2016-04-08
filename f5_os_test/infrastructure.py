# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from f5.bigip import BigIP
import pytest

from neutronclient.v2_0 import client


def pytest_addoption(parser):
    parser.addoption("--bigip", action="store",
                     help="BIG-IP hostname or IP address")
    parser.addoption("--username", action="store", help="BIG-IP REST username",
                     default="admin")
    parser.addoption("--password", action="store", help="BIG-IP REST password",
                     default="admin")
    parser.addoption('--auth_address', action='store',
                     help="Keystone Authorization server name, or IP address.")


@pytest.fixture
def bigip(request, scope="module"):
    '''bigip fixture'''
    opt_bigip = request.config.getoption("--bigip")
    opt_username = request.config.getoption("--username")
    opt_password = request.config.getoption("--password")
    b = BigIP(opt_bigip, opt_username, opt_password)
    return b


@pytest.fixture
def nclientmanager(request, polling_neutronclient):
    auth_url = 'http://%s:5000/v2.0' %\
        request.config.getoption('--auth_address')
    nclient_config = {
        'username': 'testlab',
        'password': 'changeme',
        'tenant_name': 'testlab',
        'auth_url': auth_url}

    neutronclient = client.Client(**nclient_config)
    pnc = polling_neutronclient(neutronclient)
    return pnc
