from shlib import Path, brace_expand
import pytest

def test_brace_expand_downturn():
    """brace expand"""
    # run test
    paths = brace_expand('python{2.{5..7},3.{2..5}}')

    # check
    assert set(str(p) for p in paths) == set([
        'python2.5', 'python2.6', 'python2.7',
        'python3.2', 'python3.3', 'python3.4', 'python3.5',
    ])
