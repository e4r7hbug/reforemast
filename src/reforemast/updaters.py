"""Configuration updater."""
from . import spinnaker_client


class Updater:
    """Match configurations based on criteria and apply updates."""

    @staticmethod
    def match(obj):
        """Only apply changes matching this criteria.

        Returns:
            bool: :meth:`update` should be applied to object when
            :obj:`True`.

        """
        return True

    @staticmethod
    def update(obj):
        """Apply modifications to object.

        Returns:
            obj: Spinnaker configuration with changes modified in place.

        """
        return obj

    @classmethod
    def push(cls, obj):
        """Upload changes to Spinnaker."""
        raise NotImplementedError('Subclasses must define how to upload configuration to Spinnaker.')


class ApplicationUpdater(Updater):
    """Update Spinnaker Application."""

    @classmethod
    def push(cls, application):
        """Upload changes to Spinnaker Application configuration."""
        name = application['name']

        task = {
            'application': name,
            'description': f'Update Application: {name}',
            'job': [
                {
                    'application': application,
                    'type': 'updateApplication',
                },
            ],
        }

        response = spinnaker_client.post(endpoint=f'/applications/{name}/tasks', json=task)
        return response


class PipelineUpdater(Updater):
    """Update Spinnaker Pipeline."""

    @classmethod
    def push(cls, pipeline):
        """Upload changes to Spinnaker Pipeline configuration."""
        response = spinnaker_client.post(endpoint=f'/pipelines', json=pipeline)
        return response


class StageUpdater(PipelineUpdater):
    """Update Spinnaker Pipeline Stage."""
