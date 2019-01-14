"""Reforemast global settings."""


class Settings:
    """Reforemast settings."""

    def __init__(self):
        self.gate_url = 'https://gate.spinnaker.com'

        self.application_updaters = []
        self.pipeline_updaters = []
        self.stage_updaters = []


SETTINGS = Settings()
