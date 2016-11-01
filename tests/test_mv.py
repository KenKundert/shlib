from shlib import to_path, mkdir, mv, rm, touch
import pytest

def test_mv_downturn():
    """rename file"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')

    # run test
    mv(f1, f2)

    # check
    assert f2.is_file()
    assert not f1.exists()

    # cleanup
    rm(f1, f2)

def test_mv_endorse():
    """rename file, replacing existing file"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    mv(f1, f2)

    # check
    assert f2.is_file()
    assert not f1.exists()

    # cleanup
    rm(f1, f2)

def test_mv_ground():
    """rename nonexistent file"""
    # setup
    f1 = to_path('f1')
    f2 = to_path('f2')

    # run test
    with pytest.raises(IOError):
        mv(f1, f2)

def test_mv_cymbal():
    """move two files to a new directory"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)
    d1 = to_path('d2')

    # run test
    with pytest.raises(OSError):
        mv(f1, f2, d1)

    # cleanup
    rm(f1, f2, d1)

def test_mv_gathering():
    """move file into an existing directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    f1 = to_path('f1')
    touch(f1)

    # run test
    mv(f1, d1)

    # check
    assert to_path('d1/f1').is_file()
    assert not f1.exists()

    # cleanup
    rm(d1, f1)

def test_mv_quisling():
    """move two files into an existing directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    mv(f1, f2, d1)

    # check
    assert to_path('d1/f1').is_file()
    assert to_path('d1/f2').is_file()
    assert not f1.exists()
    assert not f2.exists()

    # cleanup
    rm(d1, f1, f2)

def test_mv_liaise():
    """move two files into an existing directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    mv([f1, f2], d1)

    # check
    assert to_path('d1/f1').is_file()
    assert to_path('d1/f2').is_file()
    assert not f1.exists()
    assert not f2.exists()

    # cleanup
    rm(d1, f1, f2)

def test_mv_incense():
    """move two files into a nonexistent directory"""
    # setup
    d1 = to_path('d1')
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    with pytest.raises(OSError):
        mv([f1, f2], d1)

    # cleanup
    rm(d1, f1, f2)

def test_mv_ruminate():
    """move two files into an existing file"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)
    f3 = to_path('f2')
    touch(f3)

    # run test
    with pytest.raises(OSError):
        mv(f1, f2, f3)

    # cleanup
    rm(f1, f2, f3)

def test_mv_mobilize():
    """move directory into an existing directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    f1 = to_path('d1/f1')
    touch(f1)
    d2 = to_path('d2')
    mkdir(d2)

    # run test
    mv(d1, d2)

    # check
    assert to_path('d2/d1').is_dir()
    assert to_path('d2/d1/f1').is_file()
    assert not d1.exists()

    # cleanup
    rm(d1, d2)

def test_mv_swine():
    """rename directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    f1 = to_path('d1/f1')
    touch(f1)
    d2 = to_path('d2')

    # run test
    mv(d1, d2)

    # check
    assert to_path('d2/f1').is_file()
    assert not d1.exists()

    # cleanup
    rm(d1, d2)
