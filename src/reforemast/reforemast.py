"""Reforemast entry point."""
import logging

import click

from . import diffs, spinnaker_client
from .applications import applications
from .pipelines import pipelines
from .settings import SETTINGS

LOG = logging.getLogger(__name__)


def confirm_and_apply(updater, obj):
    """Prompt for confirmation with diff before applying changes.

    Args:
        updater (reforemast.Updater): Instance of configuration updater.
        obj (obj): Configuration object to update.

    Returns:
        bool: If the updater was applied to the object.

    """
    updated = False

    differ = diffs.DiffJson(obj)
    with differ as content:
        updater.update(content)

    highlighted_diff = differ.highlighted
    if highlighted_diff:
        click.echo(highlighted_diff)

        if click.confirm('Apply changes?'):
            updater.push(obj)
            updated = True

    return updated


class Reforemast:
    """Core Reforemast runner."""

    def __init__(self):
        self.settings = SETTINGS

    def run(self):
        """Iterate over Spinnaker Application and Pipeline configurations."""
        for application in applications():
            for application_updater in self.settings.application_updaters:
                name = application['name']

                try:
                    application_matched = application_updater.match(application)
                except KeyError as error:
                    LOG.error('Application %s is most likely not configured: %s', name, error)
                    continue

                if application_matched:

                    click.secho(f'Application: {name}', bold=True)

                    application_config = spinnaker_client.get(f'/applications/{name}')

                    confirm_and_apply(application_updater, application_config)

                    for pipeline in pipelines(application):
                        for pipeline_updater in self.settings.pipeline_updaters:
                            if pipeline_updater.match(pipeline):
                                confirm_and_apply(pipeline_updater, pipeline)

                                for stage in pipeline['stages']:
                                    for stage_updater in self.settings.stage_updaters:
                                        if stage_updater.match(stage):
                                            confirm_and_apply(stage_updater, stage)
