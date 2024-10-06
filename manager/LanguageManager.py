import gettext
import os

class LanguageManager:
    def __init__(self, default_language='zh_CN'):
        self.lang = None
        self._ = None
        self.current_language = default_language
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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