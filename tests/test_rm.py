from shlib import to_path, mkdir, rm, touch
import pytest

def test_rm_downturn():
    """remove existing file"""
    # setup
    f1 = to_path('f1')
    touch(f1)

    # run test
    rm(f1)

    # check
    assert not f1.exists()

def test_rm_endorse():
    """remove nonexistent file"""
    # setup
    f1 = to_path('f1')

    # run test
    rm(f1)

    # check
    assert not f1.exists()

def test_rm_ground():
    """remove two files"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    rm(f1, f2)

    # check
    assert not f1.exists()
    assert not f2.exists()

def test_rm_cymbal():
    """remove directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/f1')
    touch(d1f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    rm(d1, f2)

    # check
    assert not d1.exists()
    assert not f2.exists()
