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

import logging
import json

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from mgr.pub.utils.restcall import req_by_msb
from mgr.pub.config.config import REG_TO_MSB_REG_URL, REG_TO_MSB_REG_PARAM

logger = logging.getLogger(__name__)

_stub_mapping_ = {
    ("GET", "/api/ms1/v1/samples/1"): (200, {"status": "ok"})
}


class SampleList(APIView):
    def get(self, request, format=None):
        logger.debug("get")
        return Response({"status": "active"})


@api_view(http_method_names=['GET'])
def reg2msb(request, *args, **kwargs):
    ms_name = kwargs.get('msName')
    logger.info("[reg2msb]ms name is %s", ms_name)
    reg_param = REG_TO_MSB_REG_PARAM.copy()
    reg_param['serviceName'] = ms_name
    reg_param['url'] = '/api/%s/v1' % ms_name
    req_by_msb(REG_TO_MSB_REG_URL, "POST", json.JSONEncoder().encode(reg_param))
    return Response(data={"regok": ms_name}, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def reloadstub(request, *args, **kwargs):
    file_name = kwargs.get('fileName')
    logger.info("[reloadstub]file name is %s", file_name)
    global _stub_mapping_
    with open("/tmp/%s" % file_name) as url_mapping_file:
        for block in url_mapping_file.split("=##="):
            items = block.split("|")
            if len(items) != 4:
                logger.warn("Abnormal block: %s", block)
                continue
            method = items[0].strip()
            uri = items[1].strip()
            code = int(items[2].strip())
            data = json.loads(items[3].strip())
            _stub_mapping_[(method, uri)] = (code, data)


@api_view(http_method_names=['POST', 'GET', 'DELETE', 'PUT'])
def stub(request, *args, **kwargs):
    logger.info("[stub][%s][%s], data=%s", request.method, request.path, request.data)
    global _stub_mapping_
    match_result = _stub_mapping_.get((request.method.upper(), request.path))
    if match_result:
        return Response(data=match_result[1], status=match_result[0])
    return Response(data={"stub": "stub"}, status=status.HTTP_200_OK)
