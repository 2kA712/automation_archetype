import yaml


class ConfigLoader:
    _config = None

    @classmethod
    def load_config(cls, path):
        if cls._config is None:
            with open(path, "r") as file:
                cls._config = yaml.safe_load(file)
        return cls._config

    @classmethod
    def get_config(cls):
        if cls._config is None:
            raise ValueError("Configuration has not been loaded. Call load_config(path) first.")
        return cls._config
