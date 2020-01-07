# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import automl
import pytest

import get_operation_status

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]


@pytest.fixture(scope="function")
def get_operation_id():
    client = automl.AutoMlClient()
    project_location = client.location_path(PROJECT_ID, "us-central1")
    response = client.transport._operations_client.list_operations(
        project_location, ""
    )
    operation_id = ""
    for operation in response:
        operation_id = operation.name
        break
    yield operation_id


def test_get_operation_status(capsys, get_operation_id):
    get_operation_status.get_operation_status(get_operation_id)
    out, _ = capsys.readouterr()
    assert "Operation details" in out
