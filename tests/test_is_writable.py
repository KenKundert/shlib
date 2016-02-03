from shlib import is_writable, chmod, mkdir, rm, touch
import pytest

def test_is_writable_downturn():
    # setup
    touch('f1')
    mkdir('d1')

    # run tests
    chmod(0o000, 'f1')
    assert not is_writable('f1')
    chmod(0o200, 'f1')
    assert is_writable('f1')
    chmod(0o020, 'f1')
    assert not is_writable('f1')
    chmod(0o002, 'f1')
    assert not is_writable('f1')

    chmod(0o000, 'd1')
    assert not is_writable('d1')
    chmod(0o200, 'd1')
    assert is_writable('d1')
    chmod(0o020, 'd1')
    assert not is_writable('d1')
    chmod(0o002, 'd1')
    assert not is_writable('d1')

    # cleanup
    chmod(0o777, 'f1', 'd1')
    rm('f1', 'd1')
