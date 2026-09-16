import pathlib

from nodc_config import Config

def get_config_path(nodc_conf: Config, name) -> pathlib.Path:
    path = nodc_conf.get_path(name)
    if path is None:
        raise FileNotFoundError(f"nodc-config path '{name}' not found")
    return path


def get_config_directory(nodc_conf: Config, name) -> pathlib.Path:
    path = nodc_conf.get_directory(name)
    if path is None:
        raise FileNotFoundError(f"nodc-config directory '{name}' not found")
    return path
