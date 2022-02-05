import pathlib

import yaml


def load_config(path: str = None) -> dict:
    with pathlib.Path(path or "config.yml").open(encoding="utf-8") as file:
        return yaml.safe_load(file)
