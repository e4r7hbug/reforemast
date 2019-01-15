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

    def run(self):
        """Iterate over Spinnaker Application and Pipeline configurations."""
        for application in applications():
            for application_updater in self.settings.application_updaters:
                a_updater = application_updater(application)

                if a_updater.match():
                    click.secho(f'Application: {a_updater.name}', bold=True)

                    a_updater.get()

                    confirm_and_apply(a_updater, auto_apply=self.settings.auto_apply)

                    for pipeline in pipelines(application):
                        for pipeline_updater in self.settings.pipeline_updaters:
                            p_updater = pipeline_updater(pipeline)

                            if p_updater.match():
                                confirm_and_apply(p_updater, auto_apply=self.settings.auto_apply)

                                for stage in pipeline['stages']:
                                    for stage_updater in self.settings.stage_updaters:
                                        s_updater = stage_updater(stage, parent_obj=pipeline)

                                        if s_updater.match():
                                            confirm_and_apply(s_updater, auto_apply=self.settings.auto_apply)
