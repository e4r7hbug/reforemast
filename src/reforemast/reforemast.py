"""Reforemast entry point."""
import logging

import click

from .applications import applications
from .pipelines import pipelines
from .settings import SETTINGS

LOG = logging.getLogger(__name__)


def confirm_and_apply(updater, auto_apply=False):
    """Prompt for confirmation with diff before applying changes.

    Args:
        auto_apply (bool): Automatically submit changes.
        updater (reforemast.Updater): Instance of configuration updater.

    Returns:
        bool: If the updater was applied to the object.

    """
    updated = False

    LOG.debug('Applying Updater: %s', updater)

    diff = updater.diff_update()
    if diff:
        click.echo(diff)

        if auto_apply or click.confirm('Apply changes?'):
            updater.update()
            updater.push()
            updated = True

    return updated


class Reforemast:
    """Core Reforemast runner."""

    def __init__(self):
        self.settings = SETTINGS

    def matched_application_updaters(self):
        """Generate Application Updaters matching Spinnaker Applications."""
        for application in applications():
            application_matched = False

            for application_updater in self.settings.application_updaters:
                a_updater = application_updater(application)

                if a_updater.match():
                    if not application_matched:
                        click.secho(f'Application: {a_updater.name}', bold=True)
                        application_matched = True

                    a_updater.get()

                    yield a_updater

    def matched_pipeline_updaters(self, application):
        """Generate Pipeline Updaters matching Spinnaker Pipelines."""
        for pipeline in pipelines(application):
            for pipeline_updater in self.settings.pipeline_updaters:
                p_updater = pipeline_updater(pipeline)

                if p_updater.match():
                    yield p_updater

    def matched_stage_updaters(self, pipeline):
        """Generate Stage Updaters matching Spinnaker Pipelines."""
        for stage in pipeline['stages']:
            for stage_updater in self.settings.stage_updaters:
                s_updater = stage_updater(stage, parent_obj=pipeline)

                if s_updater.match():
                    yield s_updater

    def run(self):
        """Iterate over Spinnaker Application and Pipeline configurations."""
        LOG.debug('Apply Application Updaters: %s', self.settings.application_updaters)
        LOG.debug('Apply Pipeline Updaters: %s', self.settings.pipeline_updaters)
        LOG.debug('Apply Stage Updaters: %s', self.settings.stage_updaters)

        for application_updater in self.matched_application_updaters():
            confirm_and_apply(application_updater, auto_apply=self.settings.auto_apply)

            for pipeline_updater in self.matched_pipeline_updaters(application_updater.application):
                confirm_and_apply(pipeline_updater, auto_apply=self.settings.auto_apply)

                for stage_updater in self.matched_stage_updaters(pipeline_updater.pipeline):
                    confirm_and_apply(stage_updater, auto_apply=self.settings.auto_apply)
