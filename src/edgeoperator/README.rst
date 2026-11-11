Microsoft Azure CLI ``edgeoperator`` Extension
==============================================

This package provides Azure CLI commands for Azure Local Disconnected Operations.

Use ``az aldo system-readiness show`` to retrieve the current system readiness status.

The command uses the public `Microsoft.EdgeOperator SystemReadiness REST API specification <https://github.com/Azure/azure-rest-api-specs/tree/main/specification/edgeoperator/resource-manager/Microsoft.EdgeOperator/SystemReadiness>`_.

Use ``az aldo observability-configuration show`` to retrieve the active observability configuration.

The command uses the public `Microsoft.EdgeOperator ObservabilityConfiguration REST API specification <https://github.com/Azure/azure-rest-api-specs/tree/main/specification/edgeoperator/resource-manager/Microsoft.EdgeOperator/ObservabilityConfiguration>`_.

Use ``az aldo system-configuration show`` to retrieve the active system configuration.

Use ``az aldo system-configuration create`` to create or fully replace the configuration with
``--dns-forwarder-ip``, ``--connection-intent``, ``--stamp-id``, and ``--device-resource-id``.
This command uses PUT, not PATCH: omitted writable fields are not preserved. Supply all writable
values on every PUT; the service requires all four. Both commands require the Operator subscription.

The commands use the public `Microsoft.EdgeOperator SystemConfiguration REST API specification <https://github.com/Azure/azure-rest-api-specs/tree/main/specification/edgeoperator/resource-manager/Microsoft.EdgeOperator/SystemConfiguration>`_.

Use ``az aldo log-collection collect`` or ``az aldo log-collection collect-indirect`` to collect logs for a
time range. Both commands wait for completion and return the log collection job.
Use the returned ``name`` with ``show --job-id`` to view the result later.
With ``--no-wait``, both commands immediately return ``status: Accepted`` and an ``operationStatusUrl``.

To start collection and wait for the result later::

    $result = az aldo log-collection collect --from-date $from --to-date $to --no-wait | ConvertFrom-Json
    $job = az aldo log-collection wait --operation-status-url $result.operationStatusUrl | ConvertFrom-Json
    az aldo log-collection show --job-id $job.name

This wait mode returns the completed collection and reports failed or canceled operations.
Use ``--timeout`` to set the maximum wait in seconds
(default: 3600). Polling follows the service's retry interval unless ``--interval`` is supplied.
Use the same cloud and subscription as the original collection request.

To collect logs and wait for the result::

    $job = az aldo log-collection collect --from-date $from --to-date $to | ConvertFrom-Json
    az aldo log-collection show --job-id $job.name

Use ``az aldo log-collection list --from-date <date-time>`` to view job history.

The commands use the `Microsoft.EdgeOperator LogCollections REST API specification <https://github.com/Azure/azure-rest-api-specs/tree/main/specification/edgeoperator/resource-manager/Microsoft.EdgeOperator/LogCollections>`_.

Use ``az aldo billing-configuration show`` to retrieve the active billing configuration, and
``az aldo billing-configuration create`` to create or fully replace it. Pass the Azure-issued billing
configuration with ``--manifest`` to send it unchanged, which is required when it includes licenses or
signatures; otherwise, provide the individual billing arguments. Each replacement creates an immutable
snapshot; use ``az aldo billing-configuration snapshot list`` and ``snapshot show`` to view them.

The commands use the `Microsoft.EdgeOperator BillingConfigurations REST API specification <https://github.com/Azure/azure-rest-api-specs/tree/main/specification/edgeoperator/resource-manager/Microsoft.EdgeOperator/BillingConfigurations>`_.
Log collection and billing commands require the Operator subscription.

Recording scenario tests
------------------------

The scenarios under ``azext_edgeoperator/tests/latest`` use the Azure CLI test SDK.
Authenticate to AzureLocal and select the Operator subscription before recording live.
Private-cloud authentication traffic is excluded, ARM endpoints are normalized for playback,
and signed log-collection operation-status query parameters are scrubbed.

Before recording log collection, set ``FROM_DATE`` and ``TO_DATE`` in
``test_log_collection_scenario.py`` to a recent one-minute UTC interval. The direct scenario
collects logs, polls the operation, waits for the job, retrieves it, and lists job history.
Only run the indirect scenario with a valid destination and credentials.

The billing scenarios replace the active configuration and create immutable snapshots.
Run them only on an environment where those changes are intended. They cover individual
arguments and manifest submission, showing the active configuration, and listing and showing
snapshots. The manifest signature is a shape-only test fixture, not an Azure-issued signature.
