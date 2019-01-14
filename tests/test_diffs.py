"""Test diffs."""
from reforemast import diffs


def test_no_chages():
    """Verify no changes has no diff output."""
    differ = diffs.DiffJson('')

    with differ:
        pass

    result = differ.diff
    assert not result

    result = differ.highlighted
    assert not result


def test_default():
    """Default."""
    differ = diffs.DiffJson({})

    with differ as content:
        content['aksdjflksdjf'] = 'ksjdf'

    result = differ.highlighted
    assert result
