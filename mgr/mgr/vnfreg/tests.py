# Copyright 2017 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import json
import mock
from django.test import Client
from rest_framework import status

from mgr.pub.database.models import VnfRegModel
from mgr.pub.utils import restcall


class VnfRegTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        VnfRegModel.objects.filter().delete()
        self.vnfInst1 = {
            "vnfInstId": "1",
            "ip": "192.168.0.1",
            "port": "2324",
            "username": "admin",
            "password": "admin123"
        }
        self.vnfInst1_new = {
            "vnfInstId": "1",
            "ip": "192.168.0.2",
            "port": "2325",
            "username": "admin1",
            "password": "admin1234"
        }
        self.vnfconfig = {
            "vnfInstanceId": "1",
            "vnfConfigurationData": {
                "cp": [
                    {
                        "cpId": "cp-1",
                        "cpdId": "cpd-a",
                        "cpAddress": [
                            {
                                "addresses": [
                                    {
                                        "addressType": "MAC",
                                        "l2AddressData": "00:f3:43:20:a2:a3"
                                    },
                                    {
                                        "addressType": "IP",
                                        "l3AddressData": {
                                            "iPAddressType": "IPv4",
                                            "iPAddress": "192.168.104.2"
                                        }
                                    }
                                ],
                                "useDynamicAddress": "FALSE"
                            }
                        ]
                    }
                ],
                "vnfSpecificData": {
                    "autoScalable": "FALSE",
                    "autoHealable": "FALSE"
                }
            },
            "vnfcConfigurationData": {
                "vnfcId": "vnfc-1",
                "cp": [
                    {
                        "cpId": "cp-11",
                        "cpdId": "cpd-1a",
                        "cpAddress": [
                            {
                                "addresses": [
                                    {
                                        "addressType": "MAC",
                                        "l2AddressData": "00:f3:43:21:a2:a3"
                                    },
                                    {
                                        "addressType": "IP",
                                        "l3AddressData": {
                                            "iPAddressType": "IPv4",
                                            "iPAddress": "192.168.105.2"
                                        }
                                    }
                                ],
                                "useDynamicAddress": "FALSE"
                            }
                        ]
                    }
                ],
                "vnfcSpecificData": {}
            }
        }

    def tearDown(self):
        pass

    def test_add_vnf_normal(self):
        response = self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.content)
        vnfs = VnfRegModel.objects.filter()
        self.assertEqual(1, len(vnfs))
        vnfInstActual = {
            "vnfInstId": vnfs[0].id,
            "ip": vnfs[0].ip,
            "port": vnfs[0].port,
            "username": vnfs[0].username,
            "password": vnfs[0].password
        }
        self.assertEqual(self.vnfInst1, vnfInstActual)

    def test_add_vnf_when_duplicate(self):
        self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        response = self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code, response.content)
        self.assertEqual({'error': "Vnf(1) already exists."}, json.loads(response.content))

    def test_set_vnf_normal(self):
        self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        response = self.client.put("/api/vnfmgr/v1/vnfs/1",
            json.dumps(self.vnfInst1_new), content_type='application/json')
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        vnfs = VnfRegModel.objects.filter()
        self.assertEqual(1, len(vnfs))
        vnfInstActual = {
            "vnfInstId": vnfs[0].id,
            "ip": vnfs[0].ip,
            "port": vnfs[0].port,
            "username": vnfs[0].username,
            "password": vnfs[0].password
        }
        self.assertEqual(self.vnfInst1_new, vnfInstActual)

    def test_set_vnf_when_not_exist(self):
        response = self.client.put("/api/vnfmgr/v1/vnfs/1",
            json.dumps(self.vnfInst1_new), content_type='application/json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.content)
        self.assertEqual({'error': "Vnf(1) does not exist."}, json.loads(response.content))

    def test_get_vnf_normal(self):
        self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        response = self.client.get("/api/vnfmgr/v1/vnfs/1")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)
        self.assertEqual(self.vnfInst1, json.loads(response.content))

    def test_get_vnf_when_not_exist(self):
        response = self.client.get("/api/vnfmgr/v1/vnfs/1")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.content)
        self.assertEqual({'error': "Vnf(1) does not exist."}, json.loads(response.content))

    def test_del_vnf_normal(self):
        self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        response = self.client.delete("/api/vnfmgr/v1/vnfs/1")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code, response.content)

    def test_del_vnf_when_not_exist(self):
        response = self.client.delete("/api/vnfmgr/v1/vnfs/1")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.content)
        self.assertEqual({'error': "Vnf(1) does not exist."}, json.loads(response.content))

    @mock.patch.object(restcall, 'call_req')
    def test_vnf_config_normal(self, mock_call_req):
        mock_call_req.return_value = [0, "", '204']
        self.client.post("/api/vnfmgr/v1/vnfs", self.vnfInst1, format='json')
        response = self.client.post("/api/vnfmgr/v1/configuration", self.vnfconfig, format='json')
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)

    def test_vnf_config_when_not_exist(self):
        response = self.client.post("/api/vnfmgr/v1/configuration", self.vnfconfig, format='json')
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code, response.content)
        self.assertEqual({'error': "Vnf(1) does not exist."}, json.loads(response.content))
