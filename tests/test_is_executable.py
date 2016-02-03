from shlib import is_executable, chmod, mkdir, rm, touch
import pytest

def test_is_executable_downturn():
    # setup
    touch('f1')
    mkdir('d1')

    # run tests
    chmod(0o000, 'f1')
    assert not is_executable('f1')
    chmod(0o100, 'f1')
    assert is_executable('f1')
    chmod(0o010, 'f1')
    assert not is_executable('f1')
    chmod(0o001, 'f1')
    assert not is_executable('f1')

    chmod(0o000, 'd1')
    assert not is_executable('d1')
    chmod(0o100, 'd1')
    assert is_executable('d1')
    chmod(0o010, 'd1')
    assert not is_executable('d1')
    chmod(0o001, 'd1')
    assert not is_executable('d1')

    # cleanup
    chmod(0o777, 'f1', 'd1')
    rm('f1', 'd1')
