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
#

import pytest


def get_template_file(template_file):
    file = open(template_file)
    template_str = file.read()
    file.close()
    return template_str


def cleanup_stack_if_exists(heat_client, template_name):
    stacks = heat_client.stacks.list()
    for stack in stacks:
        if stack.stack_name == template_name:
            heat_client.delete_stack(stack.id)


@pytest.fixture
def HeatStack(heatclientmanager, request):
    '''Fixture for creating/deleting a heat stack.'''
    def manage_stack(template_file, template_name, parameters={}):
        def teardown():
            heatclientmanager.delete_stack(stack.id)

        template = get_template_file(template_file)
        config = {}
        config['stack_name'] = template_name
        config['template'] = template
        config['parameters'] = parameters
        # Call delete before create, in case previous teardown failed
        cleanup_stack_if_exists(heatclientmanager, template_name)
        stack = heatclientmanager.create_stack(config)
        request.addfinalizer(teardown)
        return heatclientmanager, stack
    return manage_stack
