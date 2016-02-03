from shlib import is_file, mkdir, rm, touch
import pytest

def test_if_file_downturn():
    # setup
    touch('f1')
    mkdir('d1')

    assert is_file('f1')
    assert not is_file('d1')

    # cleanup
    rm('f1', 'd1')
