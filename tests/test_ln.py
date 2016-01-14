from shlib import Path, ln, mkdir, rm, touch
import pytest

def test_ln_downturn():
    """link an existing file"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')

    # run test
    ln(f1, f2)

    # check
    assert f1.is_file()
    assert f2.is_file()
    assert f2.is_symlink()
    #assert f1.samefile(f2)

    # cleanup
    rm(f1, f2)

def test_ln_endorse():
    """link a nonexistent file"""
    # setup
    f1 = Path('f1')
    f2 = Path('f2')

    # run test
    ln(f1, f2)

    # check
    assert f2.is_symlink()

    # cleanup
    rm(f1, f2)

def test_ln_ground():
    """link to a pre-existing name"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    with pytest.raises(OSError):
        ln(f1, f2)

    # cleanup
    rm(f1, f2)

def test_ln_cymbal():
    """link an existing directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    d2 = Path('d2')

    # run test
    ln(d1, d2)

    # check
    assert d1.is_dir()
    assert d2.is_dir()
    assert d2.is_symlink()
    #assert d1.samefile(d2)

    # cleanup
    rm(d1, d2)

