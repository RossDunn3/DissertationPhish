import unittest
import pandas
import sys
sys.path.append('backend/features')
import featureEncoding

example_test_input =  [{'Link': 'http://ross.com', 'Scheme': 'http', 'IpCheck': True, 'Domain': 'ross', 'SubDomain': '', 'DomainSubcount': 1, 'Classifier': 0}, {'Link': 'https://1234.5677.1.1', 'Scheme': 'https', 'IpCheck': False, 'Domain': '1234.5677.1.1', 'SubDomain': '', 'DomainSubcount': 1, 'Classifier': 1}]

example_valid_structure_input = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'IpCheck': False, 'DomainSubcount': 1, 'keyword': 1, 'keyword_count': 1, 'length': 37, 'Classifier': 1}, {'Link': 'http://ross.google.com', 'IpCheck': False, 'DomainSubcount': 2, 'keyword' : 0, 'keyword_count': 0, 'length' : 15, 'Classifier': 0}]

example_invalid_keyword_count_structure_input = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'Scheme': 'hxxp', 'IpCheck': False, 'Domain': '', 'SubDomain': '', 'DomainSubcount': 1, 'keyword': 1, 'length': 37, 'Classifier': 1}]
example_invalid_keyword_p_structure_input = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'Scheme': 'hxxp', 'IpCheck': False, 'Domain': '', 'SubDomain': '', 'DomainSubcount': 1, 'keyword_count': 0, 'length': 37, 'Classifier': 1}]

example_invalid_hyperlink_length = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'Scheme': 'hxxp', 'IpCheck': False, 'Domain': '', 'SubDomain': '', 'DomainSubcount': 1, 'keyword': 1, 'keyword_count': 1,  'Classifier': 1}]

example_invalid_classifier = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'Scheme': 'hxxp', 'IpCheck': False, 'Domain': '', 'SubDomain': '', 'DomainSubcount': 1, 'keyword': 1, 'keyword_count': 1, 'length': 37}]

example_invalid_list_count = [{'Link': 'hxxp://???.userserve.byethost16.com/>', 'Scheme': 'hxxp', 'IpCheck': False, 'Domain': '', 'SubDomain': '',  'keyword': 1, 'keyword_count': 1, 'length': 37, 'Classifier': 1}]

example_invalid_encode_ip = [{'Link': 'http://ross.com', 'Scheme': 'http', 'Domain': 'ross', 'SubDomain': '', 'DomainSubcount': 1, 'Classifier': 0}]

#Purpose: Test suite for feature encoding functions - not all included as unneccessary -  functions can handle incorrect paramters
class TestEncodingFunctions(unittest.TestCase):
  
    def test_classifier(self):
        expected_output = pandas.DataFrame({'Classifier': [1,0]})
        actual_output = featureEncoding.get_classifer(example_valid_structure_input)   
        pandas.testing.assert_frame_equal(expected_output,actual_output) 

    def test_classifier_type(self):
        with self.assertRaisesRegex(TypeError, "Type error in classifier function"):
            output = featureEncoding.get_classifer(2)  

    #reacts to no classifier correctly
    def test_classifier_structure(self):
        expeced_output = None
        actual_output = featureEncoding.get_classifer(example_invalid_classifier)
        self.assertEqual(expeced_output, actual_output)
        
    def test_ip_encode(self):
        expected_output = pandas.DataFrame({'Ip': [1,0]})
        actual_output = featureEncoding.encode_ip(example_test_input)   
        pandas.testing.assert_frame_equal(expected_output,actual_output) 

    def test_ip_encode_type(self):
        with self.assertRaisesRegex(TypeError, "Type error in encode IP function"):
            output = featureEncoding.encode_ip(2)  

    #reacts to no classifier correctly
    def test_ip_encode_structure(self):
         with self.assertRaisesRegex(KeyError, "Key error in encode IP function"):
            output = featureEncoding.encode_ip(example_invalid_encode_ip)
    
    #as it does multiple functions, will just test the error handling - only for type as it will handle key error with empty list
    def test_encode_helper_type(self):
        with self.assertRaisesRegex(TypeError, "Type error in encoding"):
            output = featureEncoding.encoding_helper(2,'keyword','Keyword_Presence')  
 
    #error handling is done via sub functions so no need to test other than the normal input
    def test_collate_data(self):
        expected_output = pandas.DataFrame([[0,1,1,1,37,1], [0,2,0,0,15,0]], columns=['Ip', 'subDomainCount', 'Keyword_Presence', 'Keyword_count', 'length', 'Classifier'])
        actual_output = featureEncoding.collate_linkdata(example_valid_structure_input)
        pandas.testing.assert_frame_equal(expected_output, actual_output)


if __name__ == '__main__':
    print("Runnning feature encoding tests")
    unittest.main()
      