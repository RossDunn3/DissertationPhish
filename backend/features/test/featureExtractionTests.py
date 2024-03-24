import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend/features')

import featureExtraction
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

#Purpose: Testing link extraction, ham and mbox content extraction, classifier append helper and content extraction helper
class TestExtractionFunctions(unittest.TestCase):
    def test_extract_links(self):
        input_string = "blah blah http://example1.com , nonsense nonsense hxxp://example2.com , irrelevant news https://example3.com"
        #different link types test
        expected_output = [('http://example1.com', 'http'), ('hxxp://example2.com', 'hxxp'), ('https://example3.com', 'https')]
        actual_output = featureExtraction.extract_links(input_string)
        self.assertEqual(expected_output, actual_output)

    def test_extact_links_numeric_input(self):
        input_num = 5
        with self.assertRaisesRegex(TypeError, "Cannnot extract links from non-formatted input"):
            output = featureExtraction.extract_links(input_num)

    def test_subject_extraction_ham(self):
        input = email_test   
        expected_output = "Please get some bread from the shops"
        actual_output = featureExtraction.extract_subject_content_Ham(input)
        self.assertEqual(expected_output, actual_output)

    def test_subject_extraction_ham_missing_data(self):
        input = email_missing_test
        expected_output = "This is a test"
        actual_output = featureExtraction.extract_subject_content_Ham(input)
        self.assertEqual(expected_output, actual_output)   

    def test_subject_extraction_ham_numeric_input(self):
        input_num = 9
        with self.assertRaisesRegex(AttributeError, "Attribute error detected: cannot apply functions to passed argument"):
            output = featureExtraction.extract_subject_content_Ham(input_num)  

    def test_subject_extraction_mbox(self):
        input = email_test   
        expected_output = "Please get some bread from the shops"
        actual_output = featureExtraction.extract_subject_content_Mbox(input)
        self.assertEqual(expected_output, actual_output)

    def test_subject_extraction_mbox_missing_data(self):
        input = email_missing_test
        expected_output = "This is a test"
        actual_output = featureExtraction.extract_subject_content_Mbox(input)
        self.assertEqual(expected_output, actual_output)   

    def test_subject_extraction_mbox_numeric_input(self):
        input_num = 9
        with self.assertRaisesRegex(AttributeError, "Attribute error detected: cannot apply functions to passed argument"):
            output = featureExtraction.extract_subject_content_Mbox(input_num)  
    
    def test_extraction_helper(self):
        test_file = email_example
        expected_output = {'Sender': 'Joe@Bunting.com', 'Recipient': 'Mary@Bunting.com', 'Subject': 'get bread', 'Date': 'Unknown date', 'Content-Type': 'text/plain', 'Content': 'please get bread shops', 'Links': None}
        actual_output = featureExtraction.extraction_helper(test_file)
        self.assertEqual(expected_output, actual_output)

    def test_extract_helper_invalid_input(self):
        input_num = 9
        with self.assertRaisesRegex(TypeError, "Provide the correct Message input"):
            output = featureExtraction.extraction_helper(input_num)
    
    def test_append_helper(self):
        classifier = 0
        expected_output = {'Sender': 'Joe@Bunting.com', 'Recipient': 'Mary@Bunting.com', 'Subject': 'get bread', 'Date': 'Unknown date', 'Content-Type': 'text/plain', 'Content': 'please get bread shops', 'Links': None, 'Classifier': 0}
        actual_output = featureExtraction.append_helper(email_example, classifier)
        self.assertEqual(expected_output, actual_output)

    def test_append_helper_invalid_input(self):
        input_num = 9
        with self.assertRaisesRegex(TypeError, "Provide the correct Message input"):
            output = featureExtraction.append_helper(input_num, 1)
  



if __name__ == '__main__':
    print("Running feature extraction tests")
    unittest.main()
      