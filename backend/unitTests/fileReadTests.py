import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import features.readFile 
import pandas


class TestReadingFunctions(unittest.TestCase):
    # Test Purpose: Testing function abiity to read data and output in appropiate data structure
    # Mbox is not tested at this point 
    def test_alien_function(self):
        mock_input = "backend/unitTests/testingData/alienTestCsv.csv"
        actual_output = features.readFile.read_alien_data(mock_input) 
        mock_output = pandas.DataFrame({"Indicator" : ["https:example1.com/","https:example2.com/","https:example3.com/","https:example4.com/"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_alien_incorrect_file(self):
        mock_wrong_file_path = "test_not_exist"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.read_alien_data(mock_wrong_file_path)    
    
    #https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaisesRegex
    def test_alien_incorrect_paramter(self):
         mock_wrong_file_parameter = 4
         with self.assertRaisesRegex(ValueError, "Incorrect value in parameter"):
            output = features.readFile.read_alien_data(mock_wrong_file_parameter)

    def test_enron_function(self):
        mock_input = "backend/unitTests/testingData/enronTestCsv.csv"
        actual_output = features.readFile.get_enron_file(mock_input)
        mock_output = pandas.DataFrame({"file" : ["ross-w3/documents/1234."], "message" : ["This is purely testing the message section"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_enron_incorrect_paramter(self):
         mock_wrong_file_parameter = 4
         with self.assertRaisesRegex(ValueError, "Incorrect argument Value Passed"):
            output = features.readFile.get_enron_file(mock_wrong_file_parameter)

    def test_enron_incorrect_file(self):
        mock_wrong_file_path = "test_not_exist"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.get_enron_file(mock_wrong_file_path)  

    def test_data_folder_function(self):
        mock_input = "backend/unitTests/testingData/phishTest"       
        actual_output = features.readFile.read_data_folder(mock_input) 
        mock_output = ['From: Scammer\nTo: Ross\nSubject: get scammed\n\nHi Ross\n\nYou are getting scammed - http://scam.com\n\nThanks, Scammer'] 
        self.assertEqual(mock_output, actual_output)  
       
    def test_data_folder_incorrect_parameter(self):
          mock_wrong_file_parameter = 50
          with self.assertRaisesRegex(IOError, "Incorrect value in parameter"):
            output = features.readFile.read_data_folder(mock_wrong_file_parameter)

    def test_data_folder_incorrect_file(self):
        mock_wrong_file_path = "test_not_exist"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.read_data_folder(mock_wrong_file_path) 
        


if __name__ == '__main__':
    unittest.main()
      
