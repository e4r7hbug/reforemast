"""Reforemast global settings."""


class Settings:  # pylint: disable=locally-disabled,too-few-public-methods
    """Reforemast settings."""

    def __init__(self):
        self.auto_apply = False
        self.gate_url = 'https://gate.spinnaker.com'

        self.application_updaters = []
        self.pipeline_updaters = []
        self.stage_updaters = []


SETTINGS = Settings()
