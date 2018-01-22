# Copyright 2018 ZTE Corporation.
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

from rest_framework import serializers

class VnfInfoSerializer(serializers.Serializer):
    vnfInstId = serializers.CharField(help_text="the instance id of vnf", required=True)
    ip = serializers.CharField(help_text="the ip of vnf", required=True)
    port = serializers.CharField(help_text="the port of vnf", required=True)
    username = serializers.CharField(help_text="the username of vnf", required=True)
    password = serializers.CharField(help_text="the password of vnf", required=True)

class ResponseSerializer(serializers.Serializer):
    vnfInstId = serializers.CharField(help_text="the instance id of vnf", required=True)

class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="error message", required=True)
