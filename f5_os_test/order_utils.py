# Copyright 2016 F5 Networks Inc.
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


AGENT_LB_DEL_ORDER = {'/mgmt/tm/ltm/virtual':           1,
                      '/mgmt/tm/ltm/pool':              2,
                      'mgmt/tm/ltm/node/':              3,
                      'monitor':                        4,
                      'virtual-address':                5,
                      'mgmt/tm/net/self/':              6,
                      '/mgmt/tm/net/fdb':               7,
                      'mgmt/tm/net/tunnels/tunnel/':    8,
                      'mgmt/tm/net/tunnels/vxlan/':     9,
                      'mgmt/tm/net/tunnels/gre':       10,
                      'mgmt/tm/net/vlan':              11,
                      'route':                         12,
                      '/mgmt/tm/ltm/snatpool':         13,
                      '/mgmt/tm/ltm/snat-translation': 14,
                      '/mgmt/tm/net/route-domain':     15,
                      '/mgmt/tm/sys/folder':           16}


def order_by_weights(unordered, weights_table):
    '''(iterable, wieghts) --> iterable_ordered_by_weights

    AGENT_LB_DEL_ORDER is an example weights table.  Pass it as the second
    argument where the first is a list of BigIP device URIs and it will return
    a list with the resources in the appropriate order for deletion.
    Note that URIS that do not match a key in the weights table are set to have
    the same "high" weight.   Their relative order will not change.

    >>> order_by_weights([URI1, URI2, ...], AGENT_LB_DEL_ORDER)
    [URI2, URI1, ....]
    '''
    min_minus_one = min(weights_table.values()) - 1

    def order_key(item):
        for k in weights_table:
            if k in item:
                return weights_table[k]
        return min_minus_one
    ordered_by_weights = sorted(list(unordered), key=order_key)
    return ordered_by_weights
