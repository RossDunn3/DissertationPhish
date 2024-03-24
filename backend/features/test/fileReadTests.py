import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import features.readFile 
import pandas

# Test Purpose: Test correct file handling, as well as incorrect paramters and filepaths - note mbox creation not tested as returns memory address
# Fucntions - read_mbox, read_alien_data, get_enron_file, read_data_folder
class TestReadingFunctions(unittest.TestCase):
    def test_alien_function(self):
        mock_input = "backend/features/testingData/alienTestCsv.csv"
        actual_output = features.readFile.read_alien_data(mock_input) 
        mock_output = pandas.DataFrame({"Indicator" : ["https:example1.com/","https:example2.com/","https:example3.com/","https:example4.com/"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_alien_incorrect_file(self):
        mock_wrong_file_path = "/test"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.read_alien_data(mock_wrong_file_path)    
    
    #https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaisesRegex
    def test_alien_incorrect_paramter(self):
         mock_wrong_file_parameter = 4
         with self.assertRaisesRegex(ValueError, "Incorrect value in parameter"):
            output = features.readFile.read_alien_data(mock_wrong_file_parameter)

    def test_enron_function(self):
        mock_input = "backend/features/testingData/enronTestCsv.csv"
        actual_output = features.readFile.get_enron_file(mock_input)
        mock_output = pandas.DataFrame({"file" : ["ross-w3/documents/1234."], "message" : ["This is purely testing the message section"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_enron_incorrect_paramter(self):
         mock_wrong_file_parameter = 4
         with self.assertRaisesRegex(ValueError, "Incorrect argument Value Passed"):
            output = features.readFile.get_enron_file(mock_wrong_file_parameter)

    def test_enron_incorrect_file(self):
        mock_wrong_file_path = "/test"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.get_enron_file(mock_wrong_file_path)  

    def test_data_folder_function(self):
        mock_input = "backend/features/testingData/phishTest"       
        actual_output = features.readFile.read_data_folder(mock_input) 
        mock_output = ['From: Scammer\nTo: Ross\nSubject: get scammed\n\nHi Ross\n\nYou are getting scammed - http://scam.com\n\nThanks, Scammer'] 
        self.assertEqual(mock_output, actual_output)  
       
    def test_data_folder_incorrect_parameter(self):
          mock_wrong_file_parameter = 50
          with self.assertRaisesRegex(IOError, "Incorrect value in parameter"):
            output = features.readFile.read_data_folder(mock_wrong_file_parameter)

    def test_data_folder_incorrect_file(self):
        mock_wrong_file_path = "/test"
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            output = features.readFile.read_data_folder(mock_wrong_file_path) 
        
    def test_read_mbox_file_incorrect_parameter(self):
          mock_wrong_file_parameter = 50
          with self.assertRaisesRegex(TypeError, "Incorrect argument type"):
            output = features.readFile.read_mbox_file(mock_wrong_file_parameter)
    
           
    def test_read_mbox_file_incorrect_file(self):
          mock_wrong_file_parameter = "/test"
          with self.assertRaisesRegex(OSError, "Incorrect value in parameter"):
            output = features.readFile.read_mbox_file(mock_wrong_file_parameter)




if __name__ == '__main__':
    print("Running file read tests")
    unittest.main()
      
