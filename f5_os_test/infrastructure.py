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
from pprint import pprint as pp
import pytest


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

    pnc = polling_neutronclient(**nclient_config)
    return pnc


@pytest.fixture
def setup_with_nclientmanager(request, nclientmanager):
    def finalize():
        pp('Entered setup/finalize.')
        nclientmanager.delete_all_lbaas_healthmonitors()
        nclientmanager.delete_all_lbaas_pools()
        nclientmanager.delete_all_listeners()
        nclientmanager.delete_all_loadbalancers()

    finalize()
    request.addfinalizer(finalize)
    return nclientmanager


@pytest.fixture
def setup_with_loadbalancer(setup_with_nclientmanager):
    nclientmanager = setup_with_nclientmanager
    subnets = nclientmanager.list_subnets()['subnets']
    for sn in subnets:
        if 'client-v4' in sn['name']:
            lbconf = {'vip_subnet_id': sn['id'],
                      'tenant_id':     sn['tenant_id'],
                      'name':          'testlb_01'}
    activelb =\
        nclientmanager.create_loadbalancer({'loadbalancer': lbconf})
    return nclientmanager, activelb


@pytest.fixture
def setup_with_listener(setup_with_loadbalancer):
    nclientmanager, activelb = setup_with_loadbalancer
    listener_config =\
        {'listener': {'name': 'test_listener',
                      'loadbalancer_id': activelb['loadbalancer']['id'],
                      'protocol': 'HTTP',
                      'protocol_port': 80}}
    listener = nclientmanager.create_listener(listener_config)
    return nclientmanager, listener


@pytest.fixture
def setup_with_pool(setup_with_listener):
    nclientmanager, activelistener = setup_with_listener
    pool_config = {'pool': {
                   'name': 'test_pool_anur23rgg',
                   'lb_algorithm': 'ROUND_ROBIN',
                   'listener_id': activelistener['listener']['id'],
                   'protocol': 'HTTP'}}
    pool = nclientmanager.create_lbaas_pool(pool_config)
    return nclientmanager, pool


@pytest.fixture
def setup_with_pool_member(setup_with_pool):
    nclientmanager, activepool = setup_with_pool
    pool_id = activepool['pool']['id']
    for sn in nclientmanager.list_subnets()['subnets']:
        if 'server-v4' in sn['name']:
            address = sn['allocation_pools'][0]['start']
            subnet_id = sn['id']
            break

    member_config = {'member': {
                     'subnet_id': subnet_id,
                     'address': address,
                     'protocol_port': 80}}
    member = nclientmanager.create_lbaas_member(pool_id, member_config)
    return nclientmanager, activepool, member
