# Reforemast

Reformat your Spinnaker Pipelines adhoc. All of the filtering and updating
logic is meant to be kept in a separate runnable script. See
[src/reforemast/__main__.py](src/reforemast/__main__.py) for an example.

## Install

Install easily with `pip`.

```shell
$ pip install .
```

## Testing

Use `tox` to run unit testing and linting in multiple virtual environments.

```shell
$ pip install tox
$ tox
```

## Local Development

The [Pipfile](Pipfile) has been set to install the local copy as an editable
Package for faster development.

```shell
$ pipenv install
$ pipenv shell
```

## Updaters

Updaters are Classes that contain a couple predetermined Methods that are
called by Reforemast. Use different Classes for each level of configuration
and create lots of very specific updaters. This is intended to promote
smaller changes that are easier to comprehend.

Classes available to subclass are in
[src/reforemast/updaters.py](src/reforemast/updaters.py):

* ApplicationUpdater - Primarily used for updating Spinnaker Application
  configurations
* PipelineUpdater - Use to update Spinnaker Pipeline configurations outside of
  Stages
* StageUpdater - Update Pipline Stage configurations

When subclassing, override the `match` and `update` Methods.

```python
from reforemast import updaters

class EmailUpdater(updaters.ApplicationUpdater):
    """Set the email field to the Application owner."""

    def match(self):
        """All bean Applications."""
        return 'bean' in self.application['name']

    def update(self):
        """Bean Applications are owned by Ryu."""
        self.application['email'] = 'ryu@street.fighter'
        return self.application
```

If there are some variables that need to be more visible or are costly to
repeatedly generate, then attach the data as a Class Attribute.

```python
def get_application_permissions():
    """Contact IdP for permissions."""
    permissions = {}
    permissions.update(idp.get_permissions())
    return permissions


class PermissionsUpdater(updaters.ApplicationUpdater):
    """Update Application permissions to prevent accidents."""

    permissions = get_application_permissions()

    def match(self):
        """Find Applications configured in the IdP."""
        return self.application['name'] in self.permissions

    def update(self):
        """Reset permissions to match IdP."""
        name = self.application['name']
        permissions = self.permissions[name]
        self.application['attributes'].setdefault('permissions', permisions)
        return self.application
```

These should be loaded into settings for Reforemast to apply.

```python
reforemast = Reforemast()

reforemast.settings.application_updaters = [
    ApplicationUpdater1,
    EmailUpdater,
    PermissionsUpdater,
    RepoUpdater,
]

reforemast.settings.pipeline_updaters = [
    PipelineUpdater1,
    NameUpdater,
    PipelineNotificationUpdater,
    TriggerUpdater,
]

reforemast.settings.stage_updaters = [
    StageUpdater1,
    DeployNotificationUpdater,
]
```
