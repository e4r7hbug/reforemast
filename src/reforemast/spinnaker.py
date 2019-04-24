"""Spinnaker REST API calls."""
from . import spinnaker_client


def get_application(name=''):
    """Retrieve Spinnaker Application JSON.

    Args:
        name (str): Name of Spinnaker Application.

    Returns:
        dict: Configuration for Spinnaker Application.

    """
    obj = spinnaker_client.get(endpoint=f'/applications/{name}')
    attr = obj.pop('attributes')
    obj.update(attr)
    obj.pop('clusters', None)
    return obj
