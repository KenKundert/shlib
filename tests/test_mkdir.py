from shlib import Path, mkdir, rm, touch
import pytest

def test_mkdir_downturn():
    """make a directory"""
    # setup
    d1 = Path('d1')

    # run test
    mkdir(d1)

    # check
    assert d1.is_dir()

    # cleanup
    rm(d1)

def test_mkdir_endorse():
    """make two directories"""
    # setup
    d1 = Path('d1')
    d2 = Path('d2')

    # run test
    mkdir(d1, d2)

    # check
    assert d1.is_dir()
    assert d2.is_dir()

    # cleanup
    rm(d1, d2)

def test_mkdir_ground():
    """make two directories"""
    # setup
    d1 = Path('d1')
    d2 = Path('d2')

    # run test
    mkdir([d1, d2])

    # check
    assert d1.is_dir()
    assert d2.is_dir()

    # cleanup
    rm(d1, d2)

def test_mkdir_cymbal():
    """attempt to make a directory over an existing file"""
    # setup
    f1 = Path('f1')
    touch(f1)

    # run test
    with pytest.raises(OSError):
        mkdir(f1)

    # cleanup
    rm(f1)

def test_mkdir_gathering():
    """attempt to make a directory over an existing file"""
    # setup
    d1 = Path('d1')
    mkdir(d1)

    # run test
    mkdir(d1)

    # check
    assert d1.is_dir()

    # cleanup
    rm(d1)

def test_mkdir_solstice():
    """attempt to make a directory and it parent directories"""
    # setup
    d1d1 = Path('d1/d1')

    # run test
    mkdir(d1d1)

    # check
    assert d1d1.is_dir()

    # cleanup
    rm(d1d1)

def test_mkdir_brain():
    """attempt to make a directory over an existing directory"""
    # setup
    d1d1 = Path('d1/d1')
    mkdir(d1d1)

    # run test
    mkdir(d1d1)

    # check
    assert d1d1.is_dir()

    # cleanup
    rm(d1d1)
