from shlib import Path, lsf, mkdir, rm, touch
import pytest

def test_lsf_downturn():
    """list a directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d1f1 = Path('d1/f1')
    touch(d1f1)
    d1f2 = Path('d1/f2')
    touch(d1f2)
    d1d1 = Path('d1/d1')
    mkdir(d1d1)
    d1d2 = Path('d1/d2')
    mkdir(d1d2)

    # run test
    files = lsf(d1)

    # check
    assert set(str(f) for f in files) == set(['d1/f1', 'd1/f2'])

    # cleanup
    rm(d1)

def test_lsf_endorse():
    """list a directory with match constraint"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d1f1 = Path('d1/f1')
    touch(d1f1)
    d1f2 = Path('d1/f2')
    touch(d1f2)
    d1d1 = Path('d1/d1')
    mkdir(d1d1)
    d1d2 = Path('d1/d2')
    mkdir(d1d2)

    # run test
    files = lsf(d1, match='*2')

    # check
    assert set(str(f) for f in files) == set(['d1/f2'])

    # cleanup
    rm(d1)

def test_lsf_rissole():
    """list files"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    files = lsf(f1, f2)

    # check
    assert set(str(f) for f in files) == set(['f1', 'f2'])

    # cleanup
    rm(f1, f2)

def test_lsf_narrow():
    """list files with match constraint"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    files = lsf(f1, f2, match='*2')

    # check
    assert set(str(f) for f in files) == set(['f2'])

    # cleanup
    rm(f1, f2)

def test_lsf_manicure():
    """list a directory that contains dot files with match constraint"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d1f1 = Path('d1/.f1')
    touch(d1f1)
    d1f2 = Path('d1/.f2')
    touch(d1f2)
    d1d1 = Path('d1/.d1')
    mkdir(d1d1)
    d1d2 = Path('d1/.d2')
    mkdir(d1d2)

    # run test
    files = lsf(d1)

    # check
    assert set(str(f) for f in files) == set()

    # cleanup
    rm(d1)

def test_lsf_island():
    """list a directory that contains dot files with match constraint"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d1f1 = Path('d1/.f1')
    touch(d1f1)
    d1f2 = Path('d1/.f2')
    touch(d1f2)
    d1d1 = Path('d1/.d1')
    mkdir(d1d1)
    d1d2 = Path('d1/.d2')
    mkdir(d1d2)

    # run test
    files = lsf(d1, match='.*')

    # check
    assert set(str(f) for f in files) == set(['d1/.f1', 'd1/.f2'])

    # cleanup
    rm(d1)

