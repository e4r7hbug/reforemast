"""Generators for Spinnaker Applications."""
import logging

from . import spinnaker_client

LOG = logging.getLogger(__name__)


def applications():
    """Generate Spinnaker Applications."""
    _applications = spinnaker_client.get('/applications')
    for application in _applications:
        name = application['name']
        LOG.info('Application: %s', name)
        LOG.debug('Application config: %s', application)
        yield application
