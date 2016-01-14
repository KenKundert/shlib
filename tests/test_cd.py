from shlib import Path, cd, mkdir, rm, touch
import pytest

def test_cd_downturn():
    """change into directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d1f1 = Path('d1/f1')
    touch(d1f1)
    f1 = Path('f1')
    rm(f1)

    # run test
    cd(d1)

    # check
    assert f1.is_file()

def test_cd_endorse():
    """change into directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    d1f1 = 'd1/f1'
    touch(d1f1)
    f1 = 'f1'
    rm(f1)

    # run test
    cd(d1)

    # check
    assert Path(f1).is_file()
