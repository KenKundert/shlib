from shlib import is_readable, chmod, mkdir, rm, touch
import pytest

def test_is_readable_downturn():
    # setup
    touch('f1')
    mkdir('d1')

    # run tests
    chmod(0o000, 'f1')
    assert not is_readable('f1')
    chmod(0o400, 'f1')
    assert is_readable('f1')
    chmod(0o040, 'f1')
    assert not is_readable('f1')
    chmod(0o004, 'f1')
    assert not is_readable('f1')

    chmod(0o000, 'd1')
    assert not is_readable('d1')
    chmod(0o400, 'd1')
    assert is_readable('d1')
    chmod(0o040, 'd1')
    assert not is_readable('d1')
    chmod(0o004, 'd1')
    assert not is_readable('d1')

    # cleanup
    chmod(0o777, 'f1', 'd1')
    rm('f1', 'd1')
