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
    vnfInstId = serializers.CharField(
        help_text="the instance id of vnf",
        required=True,
        max_length=200,
        allow_null=True)
    ip = serializers.CharField(
        help_text="the ip of vnf",
        required=True,
        max_length=200,
        allow_null=True)
    port = serializers.CharField(
        help_text="the port of vnf",
        required=True,
        max_length=200,
        allow_null=True)
    username = serializers.CharField(
        help_text="the username of vnf",
        required=True,
        max_length=255,
        allow_null=True)
    password = serializers.CharField(
        help_text="the password of vnf",
        required=True,
        max_length=255,
        allow_null=True)


class ResponseSerializer(serializers.Serializer):
    vnfInstId = serializers.CharField(
        help_text="the instance id of vnf",
        required=True,
        max_length=200,
        allow_null=False)


class CpSerializer(serializers.Serializer):
    cpId = serializers.CharField(
        help_text="cpId",
        required=True,
        max_length=200,
        allow_null=True)
    cpdId = serializers.CharField(
        help_text="cpdId",
        required=True, max_length=200, allow_null=True)


class SpecificDataSerializer(serializers.Serializer):
    autoScalable = serializers.CharField(
        help_text="autoScalable",
        required=True,
        max_length=200,
        allow_null=True)
    autoHealable = serializers.CharField(
        help_text="autoHealable",
        required=True,
        max_length=200,
        allow_null=True)


class ConfigDataSerializer(serializers.Serializer):
    cp = CpSerializer(help_text="cps", many=True, allow_null=True)
    vnfSpecificData = SpecificDataSerializer(
        help_text="vnfSpecificData", required=True, allow_null=True)


class VnfConfigSerializer(serializers.Serializer):
    vnfInstanceId = serializers.CharField(
        help_text="vnfInstanceId",
        required=True,
        max_length=200,
        allow_null=True)
    vnfConfigurationData = ConfigDataSerializer(
        help_text="vnfConfigurationData",
        required=True,
        allow_null=True)
