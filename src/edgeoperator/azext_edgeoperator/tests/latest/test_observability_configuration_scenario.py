# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import re

from azure.cli.testsdk import JMESPathCheck, ScenarioTest
from azure.cli.testsdk.scenario_tests import RecordingProcessor


NORMALIZED_HOST = "https://management.azure.com"
_OBSERVABILITY_PATH = re.compile(
    r"^https?://[^/]+(/subscriptions/.+?/providers/Microsoft\.EdgeOperator/"
    r"observabilityConfiguration/.*)$"
)


class PrivateAuthRequestFilter(RecordingProcessor):

    def process_request(self, request):
        if (
            "autonomous.cloud.private" in request.uri
            and "observabilityConfiguration" not in request.uri
        ):
            return None
        return request


class ArmEndpointNormalizer(RecordingProcessor):

    def process_request(self, request):
        request.uri = _OBSERVABILITY_PATH.sub(
            NORMALIZED_HOST + r"\1", request.uri
        )
        return request


class ObservabilityConfigurationScenarioTest(ScenarioTest):

    def __init__(self, method_name, **kwargs):
        recording_processors = kwargs.pop("recording_processors", [])
        replay_processors = kwargs.pop("replay_processors", [])
        super().__init__(
            method_name,
            recording_processors=[
                PrivateAuthRequestFilter(),
                ArmEndpointNormalizer(),
            ]
            + recording_processors,
            replay_processors=[ArmEndpointNormalizer()] + replay_processors,
            **kwargs
        )

    def test_observability_configuration_show(self):
        result = (
            self.cmd("aldo observability-configuration show")
            .assert_with_checks(
                [
                    JMESPathCheck("name", "default"),
                    JMESPathCheck(
                        "type",
                        "Microsoft.EdgeOperator/observabilityConfiguration",
                    ),
                ]
            )
            .get_output_in_json()
        )

        properties = result["properties"]
        self.assertIsInstance(properties, dict)
        for property_value in properties.values():
            self.assertTrue(
                property_value is None or isinstance(property_value, str)
            )