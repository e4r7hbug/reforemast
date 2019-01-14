"""Spinnaker Gate requests."""
import logging

import requests

from .settings import SETTINGS

LOG = logging.getLogger(__name__)


def request(endpoint, *args, method='get', **kwargs):
    """Generic request handling."""
    url = SETTINGS.gate_url + endpoint

    requests_method = getattr(requests, method)
    response = requests_method(url, *args, **kwargs)

    response.raise_for_status()
    LOG.debug('Response: %s', response)

    return response


def get(endpoint=''):
    """GET Spinnaker request."""
    return request(endpoint, method='get').json()


def post(endpoint='', json=None):
    """POST Spinnaker request."""
    return request(endpoint, method='post', json=json).json()
