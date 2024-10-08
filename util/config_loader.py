import json
import os

class ConfigLoader:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            config_dir = os.path.join(project_root, 'config')
            config_path = os.path.join(config_dir, 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not load configuration file: {self.config_path}. Error: {e}")
            return {}

    def get(self, key, default=None):
        return self.config.get(key, default)
