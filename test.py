import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.synthetics_api import SyntheticsApi
from datadog_api_client.v1.model.synthetics_api_test import SyntheticsAPITest
from datadog_api_client.v1.model.synthetics_api_test_config import SyntheticsAPITestConfig
from datadog_api_client.v1.model.synthetics_assertion import SyntheticsAssertion
from datadog_api_client.v1.model.synthetics_assertion_operator import SyntheticsAssertionOperator
from datadog_api_client.v1.model.synthetics_assertion_type import SyntheticsAssertionType
from datadog_api_client.v1.model.synthetics_test_details_sub_type import SyntheticsTestDetailsSubType
from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
from datadog_api_client.v1.model.synthetics_test_options_retry import SyntheticsTestOptionsRetry
from datadog_api_client.v1.model.synthetics_test_request import SyntheticsTestRequest

configuration = Configuration()

with ApiClient(configuration) as api_client:
    api_instance = SyntheticsApi(api_client)

    # FIX 1: Explicitly added the 'https://' protocol schema prefix
    test_request = SyntheticsTestRequest(
        method="GET",
        url="https://dexcom.com",
        timeout=10.0
    )

    # FIX 2: Omitted the 'property' parameter for status code validations
    assertions = [
        SyntheticsAssertion(
            operator=SyntheticsAssertionOperator.IS,
            type=SyntheticsAssertionType.STATUS_CODE,
            target=200
        )
    ]

    retry_config = SyntheticsTestOptionsRetry(
        count=3,
        interval=25000
    )

    test_options = SyntheticsTestOptions(
        tick_every=60,
        min_failure_duration=0,
        min_location_failed=1,
        retry=retry_config
    )

    test_config = SyntheticsAPITestConfig(
        assertions=assertions,
        request=test_request
    )

    # FIX: Add mandatory organization tag keys
    body = SyntheticsAPITest(
        config=test_config,
        locations=["aws:eu-west-1"],
        message="Health check failed. @slack-channel",
        name="Dexcom API Health Check",
        options=test_options,
        subtype=SyntheticsTestDetailsSubType.HTTP,
        type="api",
        tags=[
            "env:production",
            "team:platform-engineering",
            "service:dexcom-integration"
        ]
    )


    try:
        response = api_instance.create_synthetics_api_test(body=body)
        print(f"Successfully created Synthetic Test ID: {response['public_id']}")
    except Exception as e:
        print(f"Exception when creating synthetic test: {e}")
