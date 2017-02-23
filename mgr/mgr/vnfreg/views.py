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

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mgr.pub.utils.values import ignore_case_get
from mgr.pub.utils.syscomm import fun_name
from mgr.pub.database.models import VnfRegModel

logger = logging.getLogger(__name__)

@api_view(http_method_names=['POST'])
def add_vnf(request, *args, **kwargs):
    logger.info("Enter %s, data is %s", fun_name(), request.data)
    vnf_inst_id = ignore_case_get(request.data, "vnfInstId")
    try:
        if VnfRegModel.objects.filter(id=vnf_inst_id):
            raise Exception("Vnf(%s) already exists." % vnf_inst_id)
        VnfRegModel(
            id=vnf_inst_id,
            ip=ignore_case_get(request.data, "ip"),
            port=ignore_case_get(request.data, "port"),
            username=ignore_case_get(request.data, "username"),
            password=ignore_case_get(request.data, "password")).save()
    except Exception as e:
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data={"vnfInstId": vnf_inst_id}, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def access_vnf(request, *args, **kwargs):
    vnf_inst_id = ignore_case_get(kwargs, "vnfInstId")
    logger.info("Enter %s, method is %s, ", fun_name(), request.method)
    logger.info("vnfInstId is %s, data is %s", vnf_inst_id, request.data)
    ret, normal_status = None, None
    try:
        vnf = VnfRegModel.objects.filter(id=vnf_inst_id)
        if not vnf:
            err_msg = "Vnf(%s) does not exist." % vnf_inst_id
            return Response(data={'error': err_msg}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            ret = {
                "vnfInstId": vnf_inst_id,
                "ip": vnf[0].ip,
                "port": vnf[0].port,
                "username": vnf[0].username,
                "password": vnf[0].password
            }
            normal_status = status.HTTP_200_OK
        elif request.method == 'PUT':
            ip = ignore_case_get(request.data, "ip")
            port = ignore_case_get(request.data, "port")
            username = ignore_case_get(request.data, "username")
            password = ignore_case_get(request.data, "password")
            if ip:
                vnf[0].ip = ip
            if port:
                vnf[0].port = port
            if username:
                vnf[0].username = username
            if password:
                vnf[0].password = password
            vnf[0].save()
            ret = {}
            normal_status = status.HTTP_202_ACCEPTED
        else:
            vnf.delete()
            ret = {}
            normal_status = status.HTTP_204_NO_CONTENT
    except Exception as e:
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret, status=normal_status)

@api_view(http_method_names=['POST'])
def vnf_config(request, *args, **kwargs):
    logger.info("Enter %s, data is %s", fun_name(), request.data)
    