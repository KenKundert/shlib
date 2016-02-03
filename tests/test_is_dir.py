from shlib import is_dir, mkdir, rm, touch
import pytest

def test_is_dir_downturn():
    # setup
    touch('f1')
    mkdir('d1')

    assert not is_dir('f1')
    assert is_dir('d1')

    # cleanup
    rm('f1', 'd1')
