from pathlib import Path


def path(schemas_name):
    return str(Path(__file__).parent.parent.joinpath(f'data/{schemas_name}'))





