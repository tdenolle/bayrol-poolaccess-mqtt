import unittest

from app.utils.Utils import normalize_string


class TestUtils(unittest.TestCase):
    def test_normalize_string(self):
        # Test case 1: Entrée normale
        input_string = "Hello, World!"
        expected_output = "hello world"
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 2: Entrée vide
        input_string = ""
        expected_output = ""
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 3: Entrée avec des caractères spéciaux
        input_string = "This is a test with @#$ special characters!"
        expected_output = "this is a test with special characters"
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 4: Entrée avec des espaces en début et fin
        input_string = "   leading and trailing spaces   "
        expected_output = "leading and trailing spaces"
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 5: Entrée avec des majuscules et minuscules mélangées
        input_string = "ThIs Is A MiXeD CaSe StRiNg"
        expected_output = "this is a mixed case string"
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 6: Entrée avec des chiffres
        input_string = "12345 numbers in the string"
        expected_output = "12345 numbers in the string"
        self.assertEqual(normalize_string(input_string), expected_output)

        # Test case 7 : Entrées avec des caractères spéciaux et caractère de remplacement
        input_string = "-This is a test with @#$ special characters!-"
        expected_output = "this-is-a-test-with-special-characters"
        self.assertEqual(normalize_string(input_string,"-"), expected_output)

if __name__ == '__main__':
    unittest.main()
