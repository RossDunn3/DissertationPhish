# Randomising data - ensures once randomised child fuctions use the same data for accuractely weighted predictions
import random
import pickle
from featureExtraction import extract_mbox, extract_ham, extract_Phish, extract_enron

#save path
filepath = "backend/features/random_data.pkl"

# retrieve content and randomise for utilising functions
def randomise_data():
    mbox = extract_mbox()
    ham = extract_ham()
    phish = extract_Phish()
    enron = extract_enron()
    combined_mail = mbox + ham + phish + enron
    random.shuffle(combined_mail) # ensure random spread of data , https://favtutor.com/blogs/shuffle-list-python
    return combined_mail

#save for use in other files
def save_random_data(filename):
    combined_mail = randomise_data()
    with open(filename, "wb") as f:
        pickle.dump(combined_mail, f)
    print("Data has been shuffled ")

save_random_data(filepath)