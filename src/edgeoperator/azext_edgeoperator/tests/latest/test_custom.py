# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from unittest import TestCase
from unittest.mock import Mock, patch

from azext_edgeoperator.custom import (
    API_VERSION,
    show_observability_configuration,
    show_system_readiness,
)


class EdgeOperatorCustomTest(TestCase):

    @patch("azext_edgeoperator.custom.send_raw_request")
    @patch("azext_edgeoperator.custom.get_subscription_id")
    def test_show_system_readiness_uses_singleton_resource(
        self, get_subscription_id, send_raw_request
    ):
        result, cli_ctx = self._run_show(
            show_system_readiness,
            get_subscription_id,
            send_raw_request,
            {"properties": {"systemReady": True}},
        )

        self._assert_singleton_request(
            send_raw_request, cli_ctx, "systemReadiness"
        )
        self.assertTrue(result["properties"]["systemReady"])

    @patch("azext_edgeoperator.custom.send_raw_request")
    @patch("azext_edgeoperator.custom.get_subscription_id")
    def test_show_observability_configuration_uses_singleton_resource(
        self, get_subscription_id, send_raw_request
    ):
        result, cli_ctx = self._run_show(
            show_observability_configuration,
            get_subscription_id,
            send_raw_request,
            {"properties": {"cloud": "AzureCloud"}},
        )

        self._assert_singleton_request(
            send_raw_request, cli_ctx, "observabilityConfiguration"
        )
        self.assertEqual("AzureCloud", result["properties"]["cloud"])

    @staticmethod
    def _run_show(operation, get_subscription_id, send_raw_request, payload):
        get_subscription_id.return_value = "00000000-0000-0000-0000-000000000000"
        response = Mock()
        response.json.return_value = payload
        send_raw_request.return_value = response

        cli_ctx = Mock()
        cli_ctx.cloud.endpoints.resource_manager = "https://management.example.com/"
        result = operation(Mock(cli_ctx=cli_ctx))
        return result, cli_ctx

    @staticmethod
    def _assert_singleton_request(send_raw_request, cli_ctx, resource_type):
        expected_url = (
            "https://management.example.com/subscriptions/"
            "00000000-0000-0000-0000-000000000000/providers/Microsoft.EdgeOperator/"
            "{}/default?api-version={}"
        ).format(resource_type, API_VERSION)
        send_raw_request.assert_called_once_with(cli_ctx, "GET", expected_url)
