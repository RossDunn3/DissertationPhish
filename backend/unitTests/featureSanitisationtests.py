import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import features.featureSanitisation

#running tests of f sanitisation fucntions

class TestSanitisationFunctions(unittest.TestCase):
    def test_removing_stopwords(self):
        input_str = "The new star wars was not good at all"
        expected_output = "new star wars good"
        actual_output = features.featureSanitisation.removing_stopwords(input_str)
        self.assertEqual(expected_output,actual_output)

    def test_stopword_invalid_input(self):
        input_num = 4
        with self.assertRaisesRegex(TypeError, "Invalid type passed to stopwords function"):
            output = features.featureSanitisation.removing_stopwords(input_num)    

    def test_tagRemoval(self):
        input_str = "<h1>This\n\\n is a test</h1>"
        expected_output = "This is a test"
        actual_output = features.featureSanitisation.remove_tags(input_str)
        self.assertEqual(expected_output,actual_output)

 

if __name__ == '__main__':
    unittest.main()
      