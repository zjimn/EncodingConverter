import gettext
import os

from util.config_loader import ConfigLoader
from util.path_util import get_base_path


class LanguageManager:
    def __init__(self, config_path='config/config.json'):
        self.lang = None
        self._ = None
        config_loader = ConfigLoader()
        self.current_language = config_loader.get('default_language', 'zh_CN')  # Fallback to 'zh_CN'
        project_root = get_base_path()
        self.localedir = os.path.join(project_root, 'locales')
        self.setup_translation()

    def setup_translation(self):
        """Set up gettext for translations."""
        gettext.bindtextdomain('messages', self.localedir)
        gettext.textdomain('messages')
        self.lang = gettext.translation('messages', self.localedir, languages=[self.current_language], fallback=True)
        self.lang.install()
        self._ = self.lang.gettext


    def switch_language(self, new_language):
        """Switch the application's language."""
        self.current_language = new_language
        self.setup_translation()  # Re-setup translation for the new language
        return self._  # Return the translation function