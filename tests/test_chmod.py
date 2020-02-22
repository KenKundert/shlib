from shlib import chmod, getmod, mkdir, rm, to_path, touch


def test_chmod_downturn():
    """change mode of a single file"""
    # setup
    f1 = to_path("f1")
    touch(f1)

    # run test
    for i in range(8):
        chmod(i, f1)
        # 0o100000 represents a regular file
        assert f1.stat().st_mode == 0o100000 + i
        assert getmod(f1) == i
        chmod(8 * i, f1)
        assert f1.stat().st_mode == 0o100000 + 8 * i
        assert getmod(f1) == 8 * i
        chmod(8 * 8 * i, f1)
        assert f1.stat().st_mode == 0o100000 + 8 * 8 * i
        assert getmod(f1) == 8 * 8 * i

    # cleanup
    rm(f1)


def test_chmod_endorse():
    """change mode of a single directory"""
    # setup
    d1 = to_path("d1")
    mkdir(d1)

    # run test
    for i in range(8):
        chmod(i, d1)
        # 0o040000 represents a directory
        assert d1.stat().st_mode == 0o040000 + i
        assert getmod(d1) == i
        chmod(8 * i, d1)
        assert d1.stat().st_mode == 0o040000 + 8 * i
        assert getmod(d1) == 8 * i
        chmod(8 * 8 * i, d1)
        assert d1.stat().st_mode == 0o040000 + 8 * 8 * i
        assert getmod(d1) == 8 * 8 * i

    # cleanup
    rm(d1)


def test_chmod_ground():
    """change mode of a single file"""
    # setup
    f1 = "f1"
    touch(f1)

    # run test
    for i in range(8):
        chmod(i, f1)
        # 0o100000 represents a regular file
        assert to_path(f1).stat().st_mode == 0o100000 + i
        assert getmod(f1) == i
        chmod(8 * i, f1)
        assert to_path(f1).stat().st_mode == 0o100000 + 8 * i
        assert getmod(f1) == 8 * i
        chmod(8 * 8 * i, f1)
        assert to_path(f1).stat().st_mode == 0o100000 + 8 * 8 * i
        assert getmod(f1) == 8 * 8 * i

    # cleanup
    rm(f1)


def test_chmod_cymbal():
    """change mode of a single directory"""
    # setup
    d1 = "d1"
    mkdir(d1)

    # run test
    for i in range(8):
        chmod(i, d1)
        # 0o040000 represents a directory
        assert to_path(d1).stat().st_mode == 0o040000 + i
        assert getmod(d1) == i
        chmod(8 * i, d1)
        assert to_path(d1).stat().st_mode == 0o040000 + 8 * i
        assert getmod(d1) == 8 * i
        chmod(8 * 8 * i, d1)
        assert to_path(d1).stat().st_mode == 0o040000 + 8 * 8 * i
        assert getmod(d1) == 8 * 8 * i

    # cleanup
    rm(d1)


def test_chmod_gathering():
    """change mode of a multiple files"""
    # setup
    f1 = to_path("f1")
    f2 = to_path("f2")
    touch(f1, f2)

    # run test
    for i in range(8):
        chmod(i, f1, f2)
        # 0o100000 represents a regular file
        assert f1.stat().st_mode == 0o100000 + i
        assert getmod(f1) == i
        assert f2.stat().st_mode == 0o100000 + i
        assert getmod(f2) == i
        chmod(8 * i, f1, f2)
        assert f1.stat().st_mode == 0o100000 + 8 * i
        assert getmod(f1) == 8 * i
        assert f2.stat().st_mode == 0o100000 + 8 * i
        assert getmod(f2) == 8 * i
        chmod(8 * 8 * i, f1, f2)
        assert f1.stat().st_mode == 0o100000 + 8 * 8 * i
        assert f2.stat().st_mode == 0o100000 + 8 * 8 * i
        assert getmod(f1) == 8 * 8 * i
        assert getmod(f2) == 8 * 8 * i

    # cleanup
    rm(f1, f2)


def test_chmod_quisling():
    """change mode of a multiple directories"""
    # setup
    d1 = to_path("d1")
    d2 = to_path("d2")
    mkdir(d1, d2)

    # run test
    for i in range(8):
        chmod(i, [d1, d2])
        # 0o040000 represents a directory
        assert d1.stat().st_mode == 0o040000 + i
        assert getmod(d1) == i
        assert d2.stat().st_mode == 0o040000 + i
        assert getmod(d2) == i
        chmod(8 * i, d1, d2)
        assert d1.stat().st_mode == 0o040000 + 8 * i
        assert getmod(d1) == 8 * i
        assert d2.stat().st_mode == 0o040000 + 8 * i
        assert getmod(d2) == 8 * i
        chmod(8 * 8 * i, d1, d2)
        assert d1.stat().st_mode == 0o040000 + 8 * 8 * i
        assert d2.stat().st_mode == 0o040000 + 8 * 8 * i
        assert getmod(d1) == 8 * 8 * i
        assert getmod(d2) == 8 * 8 * i

    # cleanup
    rm(d1)
