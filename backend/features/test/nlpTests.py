import unittest
import pandas
import sys
sys.path.append('backend/features')
import NLP

example_email = [{'Sender': 'ross@alex.com',
        'Recipient': 'alex@ross.com',
        'Subject': 'ross to alex test',
        'Date': 'Sat, 23 Sep 2024 20:52:01 -0400',
        'Content-Type': 'text/html',
        'Content': 'email about tesing with alex and ross',
        'Classifier': 0}]

example_email_invalid_key = [{'Sender': 'ross@alex.com',
        'Recipient': 'alex@ross.com',
        'Subject': 'ross to alex test',
        'Date': 'Sat, 23 Sep 2024 20:52:01 -0400',
        'Content-Type': 'text/html',
        'Contentttt': 'email about tesing with alex and ross',
        'Classifier': 0}]

#Test suite for NLP Functions
class TestNLPFunctions(unittest.TestCase):
    def test_get_language_features(self):
        expected_output = pandas.DataFrame({'Classifier': 0, 'Subject':['ross to alex test'],'Content': ['email about tesing with alex and ross']})
        actual_output = NLP.get_language_features(example_email)
        pandas.testing.assert_frame_equal(expected_output, actual_output)

    def test_get_language_features_invalid(self):
        mock_wrong_file_parameter = 4
        with self.assertRaisesRegex(TypeError, "Type error in language features"):
            output = NLP.get_language_features(mock_wrong_file_parameter)

    def test_get_language_features_invalid_key(self):
        with self.assertRaisesRegex(KeyError, "Key error in language features"):
            output = NLP.get_language_features(example_email_invalid_key)
    
    def test_get_domain_features(self):
        expected_output = pandas.DataFrame({'Classifier': 0, 'SenderDomain':['alex.com'],'ReceiverDomain': ['ross.com']})
        actual_output = NLP.get_domain_features(example_email)
        pandas.testing.assert_frame_equal(expected_output, actual_output)


if __name__ == '__main__':
    print("Runnning NLP tests")
    unittest.main()