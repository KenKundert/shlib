from shlib import cartesian_product, to_path


def test_cartesian_product_downturn():
    """empty product"""
    # run test
    paths = cartesian_product()

    # check
    assert paths == []


def test_cartesian_product_endorse():
    """cartesian product of strings"""
    # run test
    paths = cartesian_product(["A", "B", "C"], ["a", "b", "c"], "f")

    # check
    assert set(str(p) for p in paths) == set(
        [
            "A/a/f",
            "A/b/f",
            "A/c/f",
            "B/a/f",
            "B/b/f",
            "B/c/f",
            "C/a/f",
            "C/b/f",
            "C/c/f",
        ]
    )


def test_cartesian_product_negative():
    """cartesian product of paths"""
    # run test
    paths = cartesian_product(
        [to_path("A"), to_path("B"), to_path("C")], ["a", "b", "c"], "f"
    )

    # check
    assert set(str(p) for p in paths) == set(
        [
            "A/a/f",
            "A/b/f",
            "A/c/f",
            "B/a/f",
            "B/b/f",
            "B/c/f",
            "C/a/f",
            "C/b/f",
            "C/c/f",
        ]
    )
