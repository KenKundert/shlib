import sys

def pytest_ignore_collect(path):
    if str(path).endswith('extended_pathlib.py'):
        return True
    if str(path).endswith('test.clones.py'):
        return True

