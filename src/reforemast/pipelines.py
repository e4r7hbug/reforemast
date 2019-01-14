"""Generators for Spinnaker Pipelines."""
import logging

from . import spinnaker_client

LOG = logging.getLogger(__name__)


def pipelines(application):
    """Generate Spinnaker Applications."""
    application_name = application['name']
    _pipelines = spinnaker_client.get(f'/applications/{application_name}/pipelineConfigs')
    for pipeline in _pipelines:
        name = pipeline['name']
        LOG.info('Pipeline: %s', name)
        LOG.debug('Pipeline configuration: %s', pipeline)
        yield pipeline
