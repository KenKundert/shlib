from shlib import Path, cp, mkdir, rm, touch
import pytest

def test_cp_downturn():
    """copy file to new file"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')

    # run test
    cp(f1, f2)

    # check
    assert f2.is_file()

    # cleanup
    rm(f1, f2)

def test_cp_endorse():
    """copy file to existing file"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    cp(f1, f2)

    # check
    assert f2.is_file()

    # cleanup
    rm(f1, f2)

def test_cp_ground():
    """copy nonexistent file to new file"""
    # setup
    f1 = Path('f1')
    f2 = Path('f2')

    # run test
    with pytest.raises(OSError):
        cp(f1, f2)

def test_cp_cymbal():
    """copy two files to a new directory"""
    # setup
    d1 = Path('d1')
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    with pytest.raises(OSError):
        cp(f1, f2, d1)

    # cleanup
    rm(f1, f2, d1)

def test_cp_gathering():
    """copy file into an existing directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    f1 = Path('f1')
    touch(f1)

    # run test
    cp(f1, d1)

    # check
    assert Path('d1/f1').is_file()

    # cleanup
    rm(d1)

def test_cp_quisling():
    """copy two files into an existing directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    cp(f1, f2, d1)

    # check
    assert Path('d1/f1').is_file()
    assert Path('d1/f2').is_file()

    # cleanup
    rm(d1)

def test_cp_liaise():
    """copy two files into an existing directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    cp([f1, f2], d1)

    # check
    assert Path('d1/f1').is_file()
    assert Path('d1/f2').is_file()

    # cleanup
    rm(d1, f1, f2)

def test_cp_incense():
    """copy two files into a nonexistent directory"""
    # setup
    d1 = Path('d1')
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)

    # run test
    with pytest.raises(OSError):
        cp([f1, f2], d1)

    # cleanup
    rm(f1, f2)

def test_cp_ruminate():
    """copy two files into an existing file"""
    # setup
    f1 = Path('f1')
    touch(f1)
    f2 = Path('f2')
    touch(f2)
    f3 = Path('f2')
    touch(f3)

    # run test
    with pytest.raises(OSError):
        cp(f1, f2, f3)

    # cleanup
    rm(f1, f2, f3)

def test_cp_mobilize():
    """copy directory into an existing directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    f1 = Path('d1/f1')
    touch(f1)
    d2 = Path('d2')
    mkdir(d2)

    # run test
    cp(d1, d2)

    # check
    assert Path('d2/d1').is_dir()
    assert Path('d2/d1/f1').is_file()

    # cleanup
    rm(d1, d2)

def test_cp_swine():
    """copy directory into an nonexistent directory"""
    # setup
    d1 = Path('d1')
    mkdir(d1)
    f1 = Path('d1/f1')
    touch(f1)
    d2 = Path('d2')

    # run test
    cp(d1, d2)

    # check
    assert Path('d2/f1').is_file()

    # cleanup
    rm(d1, d2)

#
## Repeat the previous tests, this time using strings as arguments
#
def test_cp_demystify():
    """copy file to new file"""
    # setup
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'

    # run test
    cp(f1, f2)

    # check
    assert Path(f2).is_file()

    # cleanup
    rm(f1, f2)

def test_cp_theorem():
    """copy file to existing file"""
    # setup
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)

    # run test
    cp(f1, f2)

    # check
    assert Path(f2).is_file()

    # cleanup
    rm(f1, f2)

def test_cp_animator():
    """copy nonexistent file to new file"""
    # setup
    f1 = 'f1'
    f2 = 'f2'

    # run test
    with pytest.raises(OSError):
        cp(f1, f2)

def test_cp_adieu():
    """copy two files to a new directory"""
    # setup
    d1 = 'd1'
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)

    # run test
    with pytest.raises(OSError):
        cp(f1, f2, d1)

    # cleanup
    rm(f1, f2, d1)

def test_cp_overheat():
    """copy file into an existing directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    f1 = 'f1'
    touch(f1)

    # run test
    cp(f1, d1)

    # check
    assert Path('d1/f1').is_file()

    # cleanup
    rm(d1)

def test_cp_calculate():
    """copy two files into an existing directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)

    # run test
    cp(f1, f2, d1)

    # check
    assert Path('d1/f1').is_file()
    assert Path('d1/f2').is_file()

    # cleanup
    rm(d1)

def test_cp_hairbrush():
    """copy two files into an existing directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)

    # run test
    cp([f1, f2], d1)

    # check
    assert Path('d1/f1').is_file()
    assert Path('d1/f2').is_file()

    # cleanup
    rm(d1, f1, f2)

def test_cp_dealer():
    """copy two files into a nonexistent directory"""
    # setup
    d1 = 'd1'
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)

    # run test
    with pytest.raises(OSError):
        cp([f1, f2], d1)

    # cleanup
    rm(f1, f2)

def test_cp_attache():
    """copy two files into an existing file"""
    # setup
    f1 = 'f1'
    touch(f1)
    f2 = 'f2'
    touch(f2)
    f3 = 'f2'
    touch(f3)

    # run test
    with pytest.raises(OSError):
        cp(f1, f2, f3)

    # cleanup
    rm(f1, f2, f3)

def test_cp_headstone():
    """copy directory into an existing directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    f1 = 'd1/f1'
    touch(f1)
    d2 = 'd2'
    mkdir(d2)

    # run test
    cp(d1, d2)

    # check
    assert Path('d2/d1').is_dir()
    assert Path('d2/d1/f1').is_file()

    # cleanup
    rm(d1, d2)

def test_cp_convict():
    """copy directory into an nonexistent directory"""
    # setup
    d1 = 'd1'
    mkdir(d1)
    f1 = 'd1/f1'
    touch(f1)
    d2 = 'd2'

    # run test
    cp(d1, d2)

    # check
    assert Path('d2/f1').is_file()

    # cleanup
    rm(d1, d2)
