to_ignore = {
    'extended_pathlib.py',
    'test.clones.py',
}

def pytest_ignore_collect(collection_path, config):
    if collection_path.name in to_ignore:
        return True
