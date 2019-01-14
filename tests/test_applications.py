"""Test Application functions."""
from unittest import mock

from reforemast.applications import applications


@mock.patch('reforemast.applications.spinnaker_client')
def test_config(mock_client):
    """Validate iterating over Applications."""
    mock_client.get.return_value = [
        {
            'name': 'test',
        },
        {
            'name': 'this_test',
        },
    ]

    for application in applications():
        assert 'test' in application['name']
