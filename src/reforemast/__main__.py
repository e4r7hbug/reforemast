"""Reforemast demonstration entry point."""
import logging
import os

from reforemast import Reforemast, updaters

LOG = logging.getLogger(__name__)


class TestApplicationUpdater(updaters.ApplicationUpdater):
    """Example updater."""

    def match(self):
        """Apply updates to any test Applications."""
        return 'test' in self.name

    def update(self):
        """Overwrite the owner email."""
        self.application['email'] = 'test@example.spinnaker'


def main():
    """Entry point."""
    gate_url = os.getenv('FOREMAST_GATE_URL')

    reforemast = Reforemast()

    reforemast.settings.gate_url = gate_url

    reforemast.settings.application_updaters = [
        TestApplicationUpdater,
    ]

    reforemast.run()


if __name__ == '__main__':
    logging.basicConfig()

    LEVEL = int(os.getenv('REFOREMAST_LOG_LEVEL', str(logging.INFO)))
    LOG.setLevel(LEVEL)
    logging.getLogger('reforemast').setLevel(LEVEL)

    main()
