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
        help_text="ID of VNF instance",
        required=True,
        max_length=200,
        allow_null=True
    )
    ip = serializers.CharField(
        help_text="Ip of VNF",
        required=True,
        max_length=200,
        allow_null=True
    )
    port = serializers.CharField(
        help_text="Port of VNF",
        required=True,
        max_length=200,
        allow_null=True
    )
    username = serializers.CharField(
        help_text="Username of VNF",
        required=True,
        max_length=255,
        allow_null=True
    )
    password = serializers.CharField(
        help_text="Password of VNF",
        required=True,
        max_length=255,
        allow_null=True
    )


class ResponseSerializer(serializers.Serializer):
    vnfInstId = serializers.CharField(
        help_text="ID of VNF instance",
        required=True,
        max_length=200,
        allow_null=False
    )


class CpSerializer(serializers.Serializer):
    cpId = serializers.CharField(
        help_text="ID of CP",
        required=True,
        max_length=200,
        allow_null=True
    )
    cpdId = serializers.CharField(
        help_text="ID of CPD",
        required=True,
        max_length=200,
        allow_null=True
    )


class SpecificDataSerializer(serializers.Serializer):
    autoScalable = serializers.CharField(
        help_text="Auto scalable",
        required=True,
        max_length=200,
        allow_null=True
    )
    autoHealable = serializers.CharField(
        help_text="Auto healable",
        required=True,
        max_length=200,
        allow_null=True
    )


class ConfigDataSerializer(serializers.Serializer):
    cp = CpSerializer(
        help_text="CP list",
        many=True,
        allow_null=True
    )
    vnfSpecificData = SpecificDataSerializer(
        help_text="VNF specific data",
        required=True,
        allow_null=True
    )


class VnfConfigSerializer(serializers.Serializer):
    vnfInstanceId = serializers.CharField(
        help_text="ID of VNF instance",
        required=True,
        max_length=200,
        allow_null=True
    )
    vnfConfigurationData = ConfigDataSerializer(
        help_text="VNF configuration data",
        required=True,
        allow_null=True
    )
