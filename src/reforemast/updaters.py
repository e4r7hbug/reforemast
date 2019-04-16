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
        """Spinnaker Application configuration JSON."""
        return self.obj

    @property
    def name(self):
        """Spinnaker Application name."""
        return self.application['name']

    def get(self):
        """Retrieve Spinnaker Application configuration."""
        self.obj = spinnaker_client.get(endpoint=f'/applications/{self.name}')
        attr = self.obj.pop('attributes')
        self.obj.update(attr)
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

    def __init__(self, *args, application_name='', **kwargs):
        self.application_name = application_name

        super().__init__(*args, **kwargs)

    @property
    def name(self):
        """Spinnaker Pipeline name."""
        return self.pipeline['name']

    @property
    def pipeline(self):
        """Spinnaker Pipeline configuration JSON."""
        return self.obj

    def push(self):
        """Upload changes to Spinnaker Pipeline configuration."""
        response = spinnaker_client.post(endpoint=f'/pipelines', json=self.pipeline)
        return response


class StageUpdater(PipelineUpdater):
    """Update Spinnaker Pipeline Stage."""

    @property
    def name(self):
        """Spinnaker Pipeline Stage name."""
        return self.stage['name']

    @property
    def pipeline(self):
        """Spinnaker Pipeline configuration JSON."""
        return self.parent_obj

    @property
    def stage(self):
        """Stage configuration JSON in Spinnaker Pipeline."""
        return self.obj
