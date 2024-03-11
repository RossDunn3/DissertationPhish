import pandas as panda
import mailbox
import pandas

# Reading in mBox files 
# https://www.kaggle.com/datasets/wcukierski/enron-email-dataset
# https://docs.python.org/3/library/mailbox.html

# Reading the files for both the spam and non-spam (ham messages)

# Ammend these file paths for external use 
mbox_file_path = 'backend/trainingData/phishing3.mbox'
phish_file_path = 'backend/trainingData/IWSPA-AP-traindata/phish'
alien_file_path = 'backend/trainingData/alientVaultData.csv'
enron_file_path = 'backend/trainingData/enron_csv.csv'

# Read file and create mbox
def read_mbox_file(file_path):
    try:
        # Open the mbox file - this is in bytes format
        mbox = mailbox.mbox(file_path)
        print("New mbox created successfully")
        return mbox
    except (FileNotFoundError,ValueError) as e:
        print(e)

# https://remarkablemark.org/blog/2020/08/26/python-iterate-csv-rows/
# csv reading code abstracted to help in testing
def read_alien_data(file_path):
    try:
        alienVaultDf = pandas.read_csv(file_path)
        vaultDf = alienVaultDf.drop(columns=['Description', 'Indicator type'])
        return vaultDf
    except (FileNotFoundError,ValueError) as e:
        return e


# this dataset is considerably large (67000+) , so we will take a random subset of 0.015% between 2022-2024 - be careful of indents
def createalienVault():
    try:
        alientList = []
        vaultDf = read_alien_data(alien_file_path)
        random_vault_df = vaultDf.sample(frac=0.015, random_state=1)
        for index,rows in random_vault_df.iterrows():
            alientLink = rows['Indicator']
            alientList.append(alientLink)
        return alientList
    except (FileNotFoundError,ValueError) as e:
        return e

def get_enron_file(file_path):
    try:
        enron_df = pandas.read_csv(file_path)
        return enron_df
    except (FileNotFoundError,ValueError) as e:
        return e


# read enron dataset - consider ethical
def read_enron_file():
   try:
    enron_list = []
    enron_df = get_enron_file(enron_file_path)
    for index, rows in enron_df.iterrows():
        enron_email = rows['message']
        enron_list.append(enron_email)
    return enron_list
   except (FileNotFoundError,ValueError) as e:
        return e




