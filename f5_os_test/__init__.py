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

import random
import string

__version__ = '0.2.0'


def random_name(prefix, N):
    """Creates a name with random characters.

    Returns a new string created from an input prefix appended with a set of
    random characters. The number of random characters appended to
    the prefix string is defined by the N parameter. For example,

        random_name('test_', 6) might return "test_FR3N5Y"

    :param string prefix: String to append randoms characters.
    :param int N: Number of random characters to append.
    """
    return prefix + ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
