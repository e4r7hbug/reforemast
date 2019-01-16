"""Container for creating and displaying diffs."""
import copy
import difflib
import json

import pygments
from pygments import formatters, lexers

DIFF_LEXER = lexers.get_lexer_by_name('diff')
DIFF_FORMATTER = formatters.get_formatter_by_name('terminal16m')


class DiffText:
    """Generic text diffs."""

    def __init__(self, content):
        self.original_content = content

        self.preview = None

        self.before = None
        self.after = None

        self._diff_lines = None

    def __enter__(self):
        self.preview = copy.deepcopy(self.original_content)
        self.before = self.copy()
        return self.preview

    def __exit__(self, exc_type, exc_value, traceback):
        self.after = self.copy()

    def copy(self):
        """Duplicate string for modification."""
        return str(self.preview)

    @property
    def diff(self):
        """Generate diff."""
        _diff = difflib.unified_diff(
            self.before.split('\n'),
            self.after.split('\n'),
            fromfile='before changes',
            tofile='after changes',
            lineterm='',
        )

        self._diff_lines = list(_diff)
        return self._diff_lines

    @property
    def highlighted(self):
        """Return syntax highlighted diff."""
        diff = '\n'.join(self.diff)
        highlighted_diff = pygments.highlight(diff, DIFF_LEXER, DIFF_FORMATTER)

        highlighted_diff = highlighted_diff.rstrip('\n')

        return highlighted_diff


class DiffJson(DiffText):
    """JSON diff."""

    def copy(self):
        """Convert contents into static JSON string."""
        return json.dumps(self.preview, indent=2)
