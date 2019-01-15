"""Configuration updater."""
from . import diffs, spinnaker_client


class Updater:
    """Match configurations based on criteria and apply updates.

    Args:
        obj (object): Spinnaker Resource configuration.
        parent_obj (object): Object containing reference to :attr:`obj`, use
            case of :attr:`obj` is the Stage, then :attr:`parent_obj` would
            be the Pipeline.

    """

    def __init__(self, obj, parent_obj=None):
        self.obj = obj
        self.parent_obj = parent_obj

    def match(self):
        """Only apply changes matching this criteria.

        Returns:
            bool: :meth:`update` should be applied to object when
            :obj:`True`.

        """
        return True

    def diff_update(self):
        """Generate diff for evaluating."""
        _stash = self.obj

        differ = diffs.DiffJson(self.obj)
        with differ as content:
            self.obj = content
            self.update()
        highlighted = differ.highlighted

        self.obj = _stash

        return highlighted

    def update(self):
        """Apply modifications to object.

        Returns:
            obj: Spinnaker configuration with changes modified in place.

        """
        return self.obj

    def push(self):
        """Upload changes to Spinnaker.

        Raises:
            NotImplementedError: Subclasses must implement the appropriate
                POST call.

        """
        raise NotImplementedError('Subclasses must define how to upload configuration to Spinnaker.')


class ApplicationUpdater(Updater):
    """Update Spinnaker Application."""

    @property
    def application(self):
        return self.obj

    @property
    def name(self):
        return self.application['name']

    def get(self):
        """Retrive Spinnaker Application configuration."""
        self.obj = spinnaker_client.get(endpoint=f'/applications/{self.name}')
        return self.obj

    def push(self):
        """Upload changes to Spinnaker Application configuration."""
        task = {
            'application': self.name,
            'description': f'Update Application: {self.name}',
            'job': [
                {
                    'application': self.application,
                    'type': 'updateApplication',
                },
            ],
        }

        endpoint = f'/applications/{self.name}/tasks'
        response = spinnaker_client.post(endpoint=endpoint, json=task)
        return response


class PipelineUpdater(Updater):
    """Update Spinnaker Pipeline."""

    @property
    def pipeline(self):
        return self.obj

    def push(self):
        """Upload changes to Spinnaker Pipeline configuration."""
        response = spinnaker_client.post(endpoint=f'/pipelines', json=self.pipeline)
        return response


class StageUpdater(PipelineUpdater):
    """Update Spinnaker Pipeline Stage."""

    @property
    def pipeline(self):
        return self.parent_obj

    @property
    def stage(self):
        return self.obj
