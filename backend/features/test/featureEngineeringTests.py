import unittest
import sys
import tldextract


sys.path.append('backend/features')

import featureEngineering

#Purpose - test suite for feature engineering tests
class classTestEngineeringFunctions(unittest.TestCase):

    def test_url_len(self):
        input_url = "https://ross.test.com"
        expected_output = 21
        actual_output = featureEngineering.get_url_length(input_url)
        self.assertEqual(expected_output, actual_output)
    
    #can handle any input 
    def test_ip_checker(self):
        hyperlink = "https://210.141.1.1"
        domainExtract = tldextract.extract(hyperlink)
        domainName = domainExtract.domain
        expected_output = "210.141.1.1"
        actual_output = featureEngineering.check_url_ipPresence(domainName)
        self.assertEqual(expected_output, actual_output)
    
    def test_ip_invalid(self):
        hyperlink = "hxxp://badlink@phiser.com"
        domainExtract = tldextract.extract(hyperlink)
        domainName = domainExtract.domain
        expected_output = False
        actual_output = featureEngineering.check_url_ipPresence(domainName)
        self.assertEqual(expected_output, actual_output)

    #can handle any input
    def test_link_keywords(self):
         test_input_true = "http://ross.login@example.com"
         test_input_false = "http://normal.com"
         expected_output_true = 1
         expected_output_false = 0
         actual_output_true = featureEngineering.link_keywords(test_input_true)   
         actual_output_false = featureEngineering.link_keywords(test_input_false) 
         self.assertEqual(expected_output_true, actual_output_true)
         self.assertEqual(expected_output_false, actual_output_false)

    def test_link_keywords_count(self):
        input =  "http://ross.login@example.com"
    
        actual_output = featureEngineering.link_keywords_count(input)
        self.assertEqual(1,actual_output)
     
    def test_link_keyword_count_invalid(self):
        with self.assertRaisesRegex(AttributeError, "Invalid format passed to keyword count function"):
            output = featureEngineering.link_keywords_count(2)  

    def test_data_extraction(self):
         test_input = "hxxp://01.34.3@examplewithbadworduser.com"
         expected_output = {'Link': 'hxxp://01.34.3@examplewithbadworduser.com', 'IpCheck': False, 'Domain': 'examplewithbadworduser', 'SubDomain': '', 'DomainSubcount': 1, 'keyword': 1, 'keyword_count': 1, 'length': 41}
         actual_output = featureEngineering.data_extraction(test_input)
         self.assertEqual(expected_output, actual_output)
    
    def test_data_extraction_error(self):
        with self.assertRaisesRegex(AttributeError, "Attribute Error in data extraction function"):
            output = featureEngineering.data_extraction(2)  



if __name__ == '__main__':
    print("Running feature engineering tests")
    unittest.main()
      