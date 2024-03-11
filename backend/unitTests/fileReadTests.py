import unittest
import sys
sys.path.append('/Users/rossdunn3/Desktop/DissertationPhish/backend')
import features.readFile 
import pandas


class TestReadingFunctions(unittest.TestCase):
   # "Indicator type","Indicator","Description"
    # Test Purpose: Testing function abiity to read data and output in appropiate data structure
    def test_alien_function(self):
        mock_input = "backend/unitTests/testingData/alienTestCsv.csv"
        actual_output = features.readFile.read_alien_data(mock_input) 
        mock_output = pandas.DataFrame({"Indicator" : ["https:example1.com/","https:example2.com/","https:example3.com/","https:example4.com/"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_enron_function(self):
        mock_input = "backend/unitTests/testingData/enronTestCsv.csv"
        actual_output = features.readFile.get_enron_file(mock_input)
        mock_output = pandas.DataFrame({"file" : ["ross-w3/documents/1234."], "message" : ["This is purely testing the message section"]})
        pandas.testing.assert_frame_equal(mock_output, actual_output)

    def test_mbox_function(self):
        mock_input = ""



if __name__ == '__main__':
    unittest.main()
      
