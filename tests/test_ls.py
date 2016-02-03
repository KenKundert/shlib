from shlib import to_path, ls, mkdir, cd, rm, touch
import pytest

def test_ls_downturn():
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
    paths = ls(d1)

    # check
    assert set(str(f) for f in paths) == set(['d1/d1', 'd1/d2', 'd1/f1', 'd1/f2'])

    # cleanup
    rm(d1)

def test_ls_endorse():
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
    paths = ls(d1, select='*2')

    # check
    assert set(str(f) for f in paths) == set(['d1/d2', 'd1/f2'])

    # cleanup
    rm(d1)

def test_ls_rissole():
    """list files"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    paths = ls(f1, f2)

    # check
    assert set(str(f) for f in paths) == set(['f1', 'f2'])

    # cleanup
    rm(f1, f2)

def test_ls_narrow():
    """list files with select constraint"""
    # setup
    f1 = to_path('f1')
    touch(f1)
    f2 = to_path('f2')
    touch(f2)

    # run test
    paths = ls(f1, f2, select='*2')

    # check
    assert set(str(f) for f in paths) == set(['f2'])

    # cleanup
    rm(f1, f2)

def test_ls_manicure():
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
    paths = ls(d1)

    # check
    assert set(str(f) for f in paths) == set([])

    # cleanup
    rm(d1)

def test_ls_island():
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
    paths = ls(d1, select='.*')

    # check
    assert set(str(f) for f in paths) == set(['d1/.d1', 'd1/.d2', 'd1/.f1', 'd1/.f2'])

    # cleanup
    rm(d1)

def test_ls_nunnery():
    """list a directory that contains dot files with reject constraint"""
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
    paths = ls(d1, reject='.*')

    # check
    assert set(str(f) for f in paths) == set([])

    # cleanup
    rm(d1)

def test_ls_principle():
    """list a directory that contains dot files while retaining hidden"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/.f1')
    touch(d1f1)
    d1f2 = to_path('d1/f2')
    touch(d1f2)
    d1d1 = to_path('d1/.d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)

    # run test
    paths = ls(d1, hidden=True)

    # check
    assert set(str(f) for f in paths) == set(['d1/.d1', 'd1/d2', 'd1/.f1', 'd1/f2'])

    # cleanup
    rm(d1)

def test_ls_cadge():
    """list a directory that contains dot files while discarding hidden"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1f1 = to_path('d1/.f1')
    touch(d1f1)
    d1f2 = to_path('d1/f2')
    touch(d1f2)
    d1d1 = to_path('d1/.d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)

    # run test
    paths = ls(d1, hidden=False)

    # check
    assert set(str(f) for f in paths) == set(['d1/d2', 'd1/f2'])

    # cleanup
    rm(d1)

def test_ls_throaty():
    """recursive list of files in directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1d1 = to_path('d1/d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)
    d1d1f1 = to_path('d1/d1/f1')
    touch(d1d1f1)
    d1d2f2 = to_path('d1/d2/f2')
    touch(d1d2f2)

    # run test
    paths = ls(d1, select='**/*', only='file')

    # check
    assert set(str(f) for f in paths) == set(['d1/d1/f1', 'd1/d2/f2'])

    # cleanup
    rm(d1)

def test_ls_contrast():
    """recursive list of directories in directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)
    d1d1 = to_path('d1/d1')
    mkdir(d1d1)
    d1d2 = to_path('d1/d2')
    mkdir(d1d2)
    d1d1f1 = to_path('d1/d1/f1')
    touch(d1d1f1)
    d1d2f2 = to_path('d1/d2/f2')
    touch(d1d2f2)

    # run test
    paths = ls(d1, select='**')

    # check
    assert set(str(f) for f in paths) == set(['d1', 'd1/d1', 'd1/d2'])

    # cleanup
    rm(d1)

def test_ls_abominate():
    """recursive list of directory"""
    # setup
    mkdir('work')
    with cd('work'):
        d1 = to_path('d1')
        mkdir(d1)
        d1d1 = to_path('d1/d1')
        mkdir(d1d1)
        d1d2 = to_path('d1/d2')
        mkdir(d1d2)
        d1d1f1 = to_path('d1/d1/f1')
        touch(d1d1f1)
        d1d2f2 = to_path('d1/d2/f2')
        touch(d1d2f2)

        # run test
        paths = ls('.', select='**/*')

        # check
        assert set(str(f) for f in paths) == set(
           ['d1', 'd1/d1', 'd1/d2', 'd1/d1/f1', 'd1/d2/f2']
        )

    # cleanup
    rm('work')
