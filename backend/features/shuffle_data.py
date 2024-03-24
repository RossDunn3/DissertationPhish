# Randomising data - ensures once randomised child fuctions use the same data for accuractely weighted predictions
import random
import pickle
from featureExtraction import extract_mbox, extract_ham, extract_Phish, extract_enron

#save path
filepath = "backend/features/random_data.pkl"

#Purpose: retrieve content and randomise total email list for utilising functions
def randomise_data():
    try:
        mbox = extract_mbox()
        ham = extract_ham()
        phish = extract_Phish()
        enron = extract_enron()
        combined_mail = mbox + ham + phish + enron
        random.shuffle(combined_mail) # ensure random spread of data , https://favtutor.com/blogs/shuffle-list-python
        return combined_mail
    except Exception as e:
        raise e
    


#Purpose: Randomise email data and save for recall in NLP and Gradient boost
def save_random_data(filename):
    try:
        combined_mail = randomise_data()
        with open(filename, "wb") as f:
            pickle.dump(combined_mail, f)
        print("Data has been shuffled ")
    except FileNotFoundError:
        raise FileNotFoundError("File path does not exist")    
    except TypeError:
        raise TypeError("Invalid type passed to random data function")
    except IOError:
        raise IOError("IO Error found in random data function")

#uncomment to randomise and save data
#save_random_data(filepath)