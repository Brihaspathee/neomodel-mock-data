import os

class SecretsAPI:
    def __init__(self, keys, defaultValue=None) -> None:
        data: dict[str, str] = {}
        for key in keys:
            env_var = key.replace(".", "_").replace("-", "_").upper()
            data[key] = os.environ.get(env_var, defaultValue)
        self.data = data

    def get_secrets(self):
        return self.data