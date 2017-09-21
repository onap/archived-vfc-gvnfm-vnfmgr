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

from django.db import models


class VnfRegModel(models.Model):
    class Meta:
        db_table = 'VNF_REG'

    id = models.CharField(db_column='ID', primary_key=True, max_length=200)
    ip = models.CharField(db_column='IP', max_length=200)
    port = models.CharField(db_column='PORT', max_length=200)
    username = models.CharField(db_column='USERNAME', max_length=255)
    password = models.CharField(db_column='PASSWORD', max_length=255)
