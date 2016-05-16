#!/usr/bin/env python
# ecoding=utf-8

import http
import http_client
import requests
import unittest
from mox3 import mox

from openstack_dashboard.test.test_data import heat_data
from openstack_dashboard.test.test_data import utils


from heatclient import client as hclient
import get_auth


def heatclient():
    client = hclient.Client("1", endpoint='http://192.168.122.1:8004/v1/1acd0026829f4d28bb2eff912d7aad0d', token=get_auth.auth_token)
    print client
    return client


def snapshot_create(stack_id):
    return heatclient().stack.snapshot(stack_id)


class HttpClientTest(unittest.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        super(HttpClientTest, self).setUp()
        self.m = mox.Mox()
        # self.m.StubOutWithMock(requests, 'request')
        self.m.StubOutWithMock(hclient, 'Client')
        self.addCleanup(self.m.VerifyAll)
        self.addCleanup(self.m.UnsetStubs)

    def test_snapshot_create(self):
        heater = utils.TestData(heat_data.data)
        stack = heater.stacks.list()[0]
        stack_id = stack.id
        snapshot = heater.stack_snapshot.list()[0]

        heatclient = self.m.CreateMock(hclient.Client)
        heatclient.stacks = self.m.CreateMockAnything()
        heatclient.stacks.snapshot_create(stack_id).AndReturn(snapshot.data)

        self.m.ReplayAll()

        returned_snapshot = snapshot_create(stack_id)
        self.assertIsInstance(returned_snapshot, snapshot.data)



if __name__ == '__main__':
    unittest.main()



