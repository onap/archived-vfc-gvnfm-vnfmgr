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

from django.conf.urls import url

from mgr.vnfreg import views

urlpatterns = [
    url(r'^api/vnfmgr/v1/vnfs$', views.vnfmgr_addvnf.as_view(), name='add_vnf'),
    url(r'^api/vnfmgr/v1/vnfs/(?P<vnfInstId>[0-9a-zA-Z\-\_]+)$', views.access_vnf, name='access_vnf'),
    url(r'^api/vnfmgr/v1/configuration$', views.vnf_config, name='vnf_config'),
]
