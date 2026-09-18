# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import send_raw_request


API_VERSION = "2026-06-01-preview"


def _singleton_resource_url(cmd, resource_type):
    endpoint = cmd.cli_ctx.cloud.endpoints.resource_manager.rstrip("/")
    subscription_id = get_subscription_id(cmd.cli_ctx)
    return (
        "{}/subscriptions/{}/providers/Microsoft.EdgeOperator/"
        "{}/default?api-version={}"
    ).format(endpoint, subscription_id, resource_type, API_VERSION)


def show_system_readiness(cmd):
    response = send_raw_request(
        cmd.cli_ctx, "GET", _singleton_resource_url(cmd, "systemReadiness")
    )
    return response.json()


def show_observability_configuration(cmd):
    response = send_raw_request(
        cmd.cli_ctx,
        "GET",
        _singleton_resource_url(cmd, "observabilityConfiguration"),
    )
    return response.json()
