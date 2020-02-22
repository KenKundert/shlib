from inform import Error, Inform
from shlib import Run, set_prefs


def test_run_downturn():
    cmd = "./test_prog 0"
    p = Run(cmd, "sOEW")
    assert p.stdout == "this is stdout.\n"
    assert p.stderr == "this is stderr.\n"
    assert p.status == 0


def test_run_entree():
    cmd = "./test_prog 1"
    p = Run(cmd, "sOEW1")
    assert p.stdout == "this is stdout.\n"
    assert p.stderr == "this is stderr.\n"
    assert p.status == 1


def test_run_overlie():
    cmd = "./test_prog 3"
    p = Run(cmd, "sOEW3")
    assert p.stdout == "this is stdout.\n"
    assert p.stderr == "this is stderr.\n"
    assert p.status == 3


def test_run_layer():
    cmd = "./test_prog 3"
    p = Run(cmd, "sOEW0,3")
    assert p.stdout == "this is stdout.\n"
    assert p.stderr == "this is stderr.\n"
    assert p.status == 3


def test_run_endorse():
    cmd = "./test_prog 1"
    try:
        Run(cmd, "sOEW")
        assert False, "expected exception"
    except OSError as e:
        assert str(e) == "[Errno None] this is stderr."


def test_run_flour():
    cmd = "./test_prog 3"
    try:
        Run(cmd, "sOEW2")
        assert False, "expected exception"
    except OSError as e:
        assert str(e) == "[Errno None] this is stderr."


def test_run_parakeet():
    cmd = "./test_prog 3"
    try:
        Run(cmd, "sOEW0,1,2,4")
        assert False, "expected exception"
    except OSError as e:
        assert str(e) == "[Errno None] this is stderr."


def test_run_ground():
    Inform(prog_name=False, logfile=False)
    set_prefs(use_inform=True)
    cmd = "./test_prog 1"
    try:
        Run(cmd, "sOEW")
        assert False, "expected exception"
    except Error as e:
        assert str(e) == "this is stderr."
        assert e.cmd == "./test_prog 1"
        assert e.stdout == "this is stdout."
        assert e.stderr == "this is stderr."
        assert e.status == 1
        assert e.msg == "this is stderr."
    set_prefs(use_inform=False)
