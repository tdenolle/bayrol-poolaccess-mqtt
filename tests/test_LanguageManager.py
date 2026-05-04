#!/usr/bin/env python
import json
import os
import unittest

from app.Translation import LanguageManager


class TestLanguageManager(unittest.TestCase):

    def setUp(self):
        # Init Singleton
        LanguageManager.init()

    def test_get_string_not_setup(self):
        lang = LanguageManager()
        with self.assertRaises(RuntimeError) as context:
            lang.get_string("any_key")
        self.assertEqual(str(context.exception), "LanguageManager not setup !")

    def test_setup_success(self):
        lang = LanguageManager()
        lang.setup("fr")

        self.assertIsNotNone(lang._data)

    def test_setup_file_not_found(self):
        lang = LanguageManager()
        with self.assertRaises(FileNotFoundError):
            lang.setup("non_existing_language")

    def test_get_entity_name_success(self):
        lang = LanguageManager()
        lang.setup("fr")
        name = lang.get_string("se_activate_boost")
        self.assertEqual(name, "Boost Electrolyse")

    def test_get_string_not_found(self):
        lang = LanguageManager()
        lang.setup("en")
        with self.assertRaises(KeyError):
            lang.get_string("non_existing_key")

    def test_get_string_success_fr(self):
        lang = LanguageManager()
        lang.setup("fr")
        str = lang.get_string("al_start_delay")
        self.assertEqual(str, "Délai de démarrage")

    def test_get_string_success_en(self):
        lang = LanguageManager()
        lang.setup("en")
        str = lang.get_string("al_salt_low_cell_protection")
        self.assertEqual(str, "Salt level too low\n! Cell protection mode (low production) !")

    def test_get_string_with_default(self):
        lang = LanguageManager()
        lang.setup("en")
        str = lang.get_string("non_existing_uid", "default string")
        assert str == "default string"

    def test_all_entities_have_translations(self):
        """Verify that all entity keys in entities.json have a translation in every available language."""
        base_dir = os.path.dirname(os.path.dirname(__file__))

        # Load entities
        with open(os.path.join(base_dir, "app", "entities.json"), "r") as f:
            entities = json.load(f)
        entity_keys = [e["key"] for e in entities]

        # Discover available languages
        translations_dir = os.path.join(base_dir, "app", "translations")
        languages = [f.removesuffix(".json") for f in os.listdir(translations_dir) if f.endswith(".json")]

        missing = []
        for lang_code in sorted(languages):
            with open(os.path.join(translations_dir, f"{lang_code}.json"), "r") as f:
                translations = json.load(f)
            for key in entity_keys:
                if key not in translations:
                    missing.append(f"{lang_code}: {key}")

        self.assertEqual(missing, [], f"Missing translations:\n" + "\n".join(missing))


if __name__ == '__main__':
    unittest.main()
