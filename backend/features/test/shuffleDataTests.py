import unittest
import sys
sys.path.append('backend/features')

import shuffle_data

#unsure how to test the randomisation without manually conforming it via screenshots

#runnning tests on shuffle data operation


#Test suite for shuffle Functions

class TestShuffleFunction(unittest.TestCase):
    def test_shuffle_invalid_input(self):
        input_num = 4
        with self.assertRaisesRegex(IOError, "IO Error found in random data function"):
            output = shuffle_data.save_random_data(input_num) 

if __name__ == '__main__':
    print("Running shuffle tests")
    unittest.main()
      