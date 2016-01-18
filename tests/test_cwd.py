from shlib import to_path, cd, cwd, mkdir, rm, touch
import pytest

def test_cwd_downturn():
    """change into directory"""
    # setup
    d1 = to_path('d1')
    mkdir(d1)

    # run test
    bef = cwd()
    cd(d1)
    aft = cwd()
    delta = aft.relative_to(bef)

    # check
    assert str(delta) == 'd1'
