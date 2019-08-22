# -*- coding: utf-8 -*-
'''
    :codeauthor: Nicole Thomas <nicole@saltstack.com>
'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals
import os

# Import Salt Testing Libs
from tests.support.paths import FILES
from tests.support.helpers import expensiveTest

# Import Salt Libs
from salt.config import cloud_providers_config


# Create the cloud instance name to be used throughout the tests
from tests.integration.cloud.cloud_test_helpers import CloudTest

PROVIDER_NAME = 'joyent'


class JoyentTest(CloudTest):
    '''
    Integration tests for the Joyent cloud provider in Salt-Cloud
    '''

    @expensiveTest
    def setUp(self):
        '''
        Sets up the test requirements
        '''
        super(JoyentTest, self).setUp()

        # check if appropriate cloud provider and profile files are present
        profile_str = 'joyent-config'
        providers = self.run_cloud('--list-providers')
        if profile_str + ':' not in providers:
            self.skipTest(
                'Configuration file for {0} was not found. Check {0}.conf files '
                'in tests/integration/files/conf/cloud.*.d/ to run these tests.'
                    .format(PROVIDER_NAME)
            )

        # check if user, password, private_key, and keyname are present
        config = cloud_providers_config(
            os.path.join(
                FILES,
                'conf',
                'cloud.providers.d',
                PROVIDER_NAME + '.conf'
            )
        )

        user = config[profile_str][PROVIDER_NAME]['user']
        password = config[profile_str][PROVIDER_NAME]['password']
        private_key = config[profile_str][PROVIDER_NAME]['private_key']
        keyname = config[profile_str][PROVIDER_NAME]['keyname']

        if user == '' or password == '' or private_key == '' or keyname == '':
            self.skipTest(
                'A user name, password, private_key file path, and a key name '
                'must be provided to run these tests. Check '
                'tests/integration/files/conf/cloud.providers.d/{0}.conf'
                    .format(PROVIDER_NAME)
            )

        self.assertEqual(self._instance_exists(), False,
                         'The instance "{}" exists before it was created by the test'.format(self.INSTANCE_NAME))

    def test_instance(self):
        '''
        Test creating and deleting instance on Joyent
        '''
        self.assertIn(
            self.INSTANCE_NAME,
            [i.strip() for i in self.run_cloud('-p joyent-test {0}'.format(self.INSTANCE_NAME), timeout=500)]
        )
        self.assertEqual(self._instance_exists(), True)

    def tearDown(self):
        self._destroy_instance()
