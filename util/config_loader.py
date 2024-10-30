import json
import os

from util.path_util import get_base_path


class ConfigLoader:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        config_path = ""
        try:
            project_root = get_base_path()
            config_dir = os.path.join(project_root, 'config')
            config_path = os.path.join(config_dir, 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not load configuration file: {config_path}. Error: {e}")
            return {}

    def get(self, key, default=None):
        return self.config.get(key, default)
