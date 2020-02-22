from shlib import cd, cwd, mkdir, rm, to_path


def test_cwd_downturn():
    """change into directory"""
    # setup
    d1 = to_path("d1")
    mkdir(d1)

    # run test
    bef = cwd()
    with cd(d1):
        aft = cwd()
        delta = aft.relative_to(bef)
        assert str(delta) == "d1"

    # cleanup
    rm(d1)
