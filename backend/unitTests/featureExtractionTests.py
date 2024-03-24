import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import features.readFile
import features.featureExtraction
from email import message_from_string

email_example = """\
From: Joe@Bunting.com
To: Mary@Bunting.com
Subject: Get Bread
Content-Type: text/plain

Please get some bread from the shops"""

example_email_missing = """\
From: Ross@test.com

This is a test"""
email_test = message_from_string(email_example)
email_missing_test = message_from_string(example_email_missing)

# running tests on the f extraction child functions, manual testing on larger complex functions

class TestExtractionFunctions(unittest.TestCase):
    # testing child extraction functions
    #extract links is ran on string extracted from a file
    def test_extract_links(self):
        input_string = "blah blah http://example1.com , nonsense nonsense hxxp://example2.com , irrelevant news https://example3.com"
        #different link types test
        expected_output = [('http://example1.com', 'http'), ('hxxp://example2.com', 'hxxp'), ('https://example3.com', 'https')]
        actual_output = features.featureExtraction.extract_links(input_string)
        self.assertEqual(expected_output, actual_output)

    def test_extact_links_numeric_input(self):
        input_num = 5
        with self.assertRaisesRegex(TypeError, "Cannnot extract links from non-formatted input"):
            output = features.featureExtraction.extract_links(input_num)

    def test_subject_extraction(self):
        input = email_test   
        expected_output = "Please get some bread from the shops"
        actual_output = features.featureExtraction.extract_subject_content_Ham(input)
        self.assertEqual(expected_output, actual_output)

    def test_subject_extraction_missing_data(self):
        input = email_missing_test
        expected_output = "This is a test"
        actual_output = features.featureExtraction.extract_subject_content_Ham(input)
        self.assertEqual(expected_output, actual_output)   

    def test_subject_extraction_numeric_input(self):
        input_num = 9
        with self.assertRaisesRegex(AttributeError, "Attribute error detected: cannot apply functions to passed argument"):
            output = features.featureExtraction.extract_subject_content_Ham(input_num)    



if __name__ == '__main__':
    unittest.main()
      