from shlib import Path, touch, rm
import pytest

def test_touch_downturn():
    """touch an existing file"""
    # setup
    f1 = Path('f1')
    touch(f1)

    # run test
    touch(f1)

    # check
    assert f1.is_file()

    # cleanup
    rm(f1)

def test_touch_endorse():
    """touch a new file"""
    # setup
    f1 = Path('f1')

    # run test
    touch(f1)

    # check
    assert f1.is_file()

    # cleanup
    rm(f1)

def test_touch_ground():
    """touch multiple files"""
    # setup
    f1 = Path('f1')
    f2 = Path('f2')

    # run test
    touch(f1, f2)

    # check
    assert f1.is_file()
    assert f2.is_file()

    # cleanup
    rm(f1, f2)

def test_touch_cymbal():
    """touch multiple files"""
    # setup
    f1 = Path('f1')
    f2 = Path('f2')

    # run test
    touch([f1, f2])

    # check
    assert f1.is_file()
    assert f2.is_file()

    # cleanup
    rm(f1, f2)
