import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import unittest
import features.featureEngineering


# running tests on the f engineering child functions, manual testing on larger complex functions

class TestEngineeringFunctions(unittest.TestCase):
    def test_get_url_length(self):
        url = "https://ross.dunn.com"
        expected_result = 21
        actual_output = features.featureEngineering.get_url_length(url)
        self.assertEqual(expected_result, actual_output)

    def test_check_url_ipPresence_true(self):
        url = "192.168.1.1"
        actual_output = features.featureEngineering.check_url_ipPresence(url)
        self.assertEqual("192.168.1.1", actual_output)
    
    def test_check_url_ipPresence_false(self):
        url = "http://link.com"
        actual_output = features.featureEngineering.check_url_ipPresence(url)
        self.assertEqual(False, actual_output)

    def test_link_keywords_valid(self):
        url = "http://login.com"
        actual_output = features.featureEngineering.link_keywords(url)
        self.assertEqual(1, actual_output)

    def test_link_keywords_invalid(self):
        url = 4
        actual_output = features.featureEngineering.link_keywords(url)
        self.assertEqual(0, actual_output)

    def test_keyword_count_present(self):
         url = "http://login.account.com"
         actual_output = features.featureEngineering.link_keywords_count(url)
         self.assertEqual(2, actual_output)

    def test_keyword_count_present_invalid(self):
        input_num = 9
        with self.assertRaisesRegex(AttributeError, "Invalid format passed to keyword count function"):
            output = features.featureEngineering.link_keywords_count(input_num)  

if __name__ == '__main__':
    unittest.main()
      