import json
import os


class Singleton(type):
    _instances = {}

    def init(cls):
        cls._instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LanguageManager(metaclass=Singleton):
    def __init__(self):
        self._data = None

    def setup(self, language: str):
        # load language file
        filepath = os.path.join(os.path.dirname(__file__), "translations", "%s.json" % language)
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)

        with open(filepath, 'r') as fp:
            self._data = json.load(fp)

    def _assert_setup(self):
        if not self._data:
            raise RuntimeError("LanguageManager not setup !")

    def get_string(self, key: str, default: str = None):
        self._assert_setup()
        if key not in self._data and default is not None:
            return default
        return self._data[key]
