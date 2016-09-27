from shlib import to_path, cd, mkdir, rm, touch, cwd
import pytest

def test_cd_downturn():
    """change into directory"""
    # setup
    dot = cwd()
    d1 = to_path('d1')
    mkdir(d1)
    d1p = to_path(d1).resolve()
    d1f1 = to_path('d1/f1')
    touch(d1f1)
    f1 = to_path('f1')
    rm(f1)

    # run test
    cd(d1)
    assert to_path(f1).is_file()
    assert str(d1p) == str(cwd())
    cd('..')
    assert str(dot) == str(cwd())

    # clean up
    rm(d1)

def test_cd_endorse():
    """change into directory"""
    # setup
    dot = cwd()
    d1 = 'd1'
    mkdir(d1)
    d1p = to_path(d1).resolve()
    d1f1 = 'd1/f1'
    touch(d1f1)
    f1 = 'f1'
    rm(f1)

    # run test
    cd(d1)
    assert to_path(f1).is_file()
    assert str(d1p) == str(cwd())
    cd('..')
    assert str(dot) == str(cwd())

    # clean up
    rm(d1)

def test_cd_thinner():
    """change into directory"""
    # setup
    dot = cwd()
    d1 = to_path('d1')
    mkdir(d1)
    d1p = to_path(d1).resolve()
    d1f1 = to_path('d1/f1')
    touch(d1f1)
    f1 = to_path('f1')
    rm(f1)

    # run test
    with cd(d1):
        assert to_path(f1).is_file()
        assert str(d1p) == str(cwd())
    assert str(dot) == str(cwd())

    # clean up
    rm(d1)

def test_cd_quoit():
    """change into directory"""
    # setup
    dot = cwd()
    d1 = 'd1'
    mkdir(d1)
    d1p = to_path(d1).resolve()
    d1f1 = 'd1/f1'
    touch(d1f1)
    f1 = 'f1'
    rm(f1)

    # run test
    with cd(d1):
        assert to_path(f1).is_file()
        assert str(d1p) == str(cwd())
    assert str(dot) == str(cwd())

    # clean up
    rm(d1)
