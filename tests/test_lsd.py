from shlib import to_path, lsd, mkdir, rm, touch
import pytest

def test_lsd_downturn():
    """list a directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/f1')
    touch(d1f1)
    d1f2 = to_path('d1/f2')
    touch(d1f2)
    d1d1 = to_path('d1/d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)

    # run test
    files = lsd(d1)

    # check
    assert set(str(f) for f in files) == set(['d1/d1', 'd1/d2'])

    # cleanup
    rm(d1)

def test_lsd_endorse():
    """list a directory with select constraint"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/f1')
    touch(d1f1)
    d1f2 = to_path('d1/f2')
    touch(d1f2)
    d1d1 = to_path('d1/d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)

    # run test
    files = lsd(d1, select='*2')

    # check
    assert set(str(f) for f in files) == set(['d1/d2'])

    # cleanup
    rm(d1)

def test_lsd_rissole():
    """list files"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    files = lsd(f1, f2)

    # check
    assert set(str(f) for f in files) == set()

    # cleanup
    rm(f1, f2)

def test_lsd_narrow():
    """list files with select constraint"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    files = lsd(f1, f2, select='*2')

    # check
    assert set(str(f) for f in files) == set()

    # cleanup
    rm(f1, f2)

def test_lsd_manicure():
    """list a directory that contains dot files with select constraint"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/.f1')
    touch(d1f1)
    d1f2 = to_path('d1/.f2')
    touch(d1f2)
    d1d1 = to_path('d1/.d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/.d2')
    mkdir(d1d2)

    # run test
    files = lsd(d1)

    # check
    assert set(str(f) for f in files) == set()

    # cleanup
    rm(d1)

def test_lsd_island():
    """list a directory that contains dot files with select constraint"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/.f1')
    touch(d1f1)
    d1f2 = to_path('d1/.f2')
    touch(d1f2)
    d1d1 = to_path('d1/.d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/.d2')
    mkdir(d1d2)

    # run test
    files = lsd(d1, select='.*')

    # check
    assert set(str(f) for f in files) == set(['d1/.d1', 'd1/.d2'])

    # cleanup
    rm(d1)

