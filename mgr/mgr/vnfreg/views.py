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

import json
import logging
import traceback

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from mgr.pub.database.models import VnfRegModel
from mgr.pub.utils import restcall
from mgr.pub.utils.syscomm import fun_name
from mgr.pub.utils.values import ignore_case_get
from mgr.vnfreg.serializers import VnfInfoSerializer, ResponseSerializer, NoneSerializer, VnfConfigSerializer

logger = logging.getLogger(__name__)


class vnfmgr_addvnf(APIView):
    @swagger_auto_schema(request_body=VnfInfoSerializer(),
                         responses={
                             status.HTTP_201_CREATED: ResponseSerializer(),
                             status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
    def post(self, request):
        logger.info("Enter %s, data is %s", fun_name(), request.data)
        requestSerializer = VnfInfoSerializer(data=request.data)
        request_isValid = requestSerializer.is_valid()
        try:
            if not request_isValid:
                raise Exception(requestSerializer.errors)

            requestData = requestSerializer.data
            vnf_inst_id = ignore_case_get(requestData, "vnfInstId")
            if VnfRegModel.objects.filter(id=vnf_inst_id):
                raise Exception("Vnf(%s) already exists." % vnf_inst_id)
            VnfRegModel(
                id=vnf_inst_id,
                ip=ignore_case_get(requestData, "ip"),
                port=ignore_case_get(requestData, "port"),
                username=ignore_case_get(requestData, "username"),
                password=ignore_case_get(requestData, "password")).save()

            responseSerializer = ResponseSerializer(data={"vnfInstId": vnf_inst_id})
            isValid = responseSerializer.is_valid()
            if not isValid:
                raise Exception(responseSerializer.errors)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=responseSerializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='put',
                     request_body=VnfInfoSerializer(),
                     responses={
                         status.HTTP_202_ACCEPTED: NoneSerializer(),
                         status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
@swagger_auto_schema(method='delete',
                     responses={
                         status.HTTP_204_NO_CONTENT: NoneSerializer(),
                         status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
@swagger_auto_schema(methods=['get'],
                     manual_parameters=[
                         openapi.Parameter('test',
                                           openapi.IN_QUERY,
                                           "test manual param",
                                           type=openapi.TYPE_BOOLEAN
                                           ), ],
                     responses={
                         status.HTTP_200_OK: openapi.Response('response description', VnfInfoSerializer()),
                         status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def access_vnf(request, *args, **kwargs):
    requestSerializer = VnfInfoSerializer(data=request.data)
    request_isValid = requestSerializer.is_valid()
    vnf_inst_id = ignore_case_get(kwargs, "vnfInstId")
    logger.info("Enter %s, method is %s, ", fun_name(), request.method)
    logger.info("vnfInstId is %s, data is %s", vnf_inst_id, request.data)
    try:
        vnf = VnfRegModel.objects.filter(id=vnf_inst_id)
        if not vnf:
            err_msg = "Vnf(%s) does not exist." % vnf_inst_id
            return Response(data={'error': err_msg}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            resp = {
                "vnfInstId": vnf_inst_id,
                "ip": vnf[0].ip,
                "port": vnf[0].port,
                "username": vnf[0].username,
                "password": vnf[0].password
            }
            responseSerializer = VnfInfoSerializer(data=resp)
            if not responseSerializer.is_valid():
                raise Exception(responseSerializer.errors)
            ret = responseSerializer.data
            normal_status = status.HTTP_200_OK
        elif request.method == 'PUT':
            if not request_isValid:
                raise Exception(requestSerializer.errors)

            requestData = requestSerializer.data
            ip = ignore_case_get(requestData, "ip")
            port = ignore_case_get(requestData, "port")
            username = ignore_case_get(requestData, "username")
            password = ignore_case_get(requestData, "password")
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
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret, status=normal_status)


@swagger_auto_schema(method='post',
                     request_body=VnfConfigSerializer(),
                     responses={
                         status.HTTP_202_ACCEPTED: NoneSerializer(),
                         status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal error'})
@api_view(http_method_names=['POST'])
def vnf_config(request, *args, **kwargs):
    logger.info("Enter %s, data is %s", fun_name(), request.data)
    requestSerializer = VnfConfigSerializer(data=request.data)
    request_isValid = requestSerializer.is_valid()
    try:
        if not request_isValid:
            raise Exception(requestSerializer.errors)

        requestData = requestSerializer.data
        vnf_inst_id = ignore_case_get(requestData, "vnfInstanceId")
        vnf = VnfRegModel.objects.filter(id=vnf_inst_id)
        if not vnf:
            raise Exception("Vnf(%s) does not exist." % vnf_inst_id)
        ret = restcall.call_req(
            base_url="http://%s:%s/" % (vnf[0].ip, vnf[0].port),
            user=vnf[0].username,
            passwd=vnf[0].password,
            auth_type=restcall.rest_no_auth,
            resource="v1/vnfconfig",
            method="POST",
            content=json.dumps(requestData))
        if ret[0] != 0:
            raise Exception("Failed to config Vnf(%s): %s" % (vnf_inst_id, ret[1]))
    except Exception as e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data={}, status=status.HTTP_202_ACCEPTED)
