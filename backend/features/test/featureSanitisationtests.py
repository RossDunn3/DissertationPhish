import unittest
import sys
sys.path.append('backend/features')
import featureSanitisation


#Purpose: Testing the stop word removal and tag removal functions, as well as invalid inputs for stopword removal
class TestSanitisationFunctions(unittest.TestCase):
    def test_removing_stopwords(self):
        input_str = "The new star wars was not good at all"
        expected_output = "new star wars good"
        actual_output = featureSanitisation.removing_stopwords(input_str)
        self.assertEqual(expected_output,actual_output)

    def test_stopword_invalid_input(self):
        input_num = 4
        with self.assertRaisesRegex(TypeError, "Invalid type passed to stopwords function"):
            output = featureSanitisation.removing_stopwords(input_num)    


    def test_tagRemoval(self):
        input_str = "<h1>This\n\\n is a test</h1>"
        expected_output = "This is a test"
        actual_output = featureSanitisation.remove_tags(input_str)
        self.assertEqual(expected_output,actual_output)

        #tag word removal can handle any form of input, returning input as string
    def test_tagRemoval_invaid(self):
        expected_output = '50'
        actual_output = featureSanitisation.remove_tags(50)
        self.assertEqual(expected_output,actual_output)
    

 

if __name__ == '__main__':
    print("Running feature sanitisation tests")
    unittest.main()
      