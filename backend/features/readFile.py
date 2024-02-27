import pandas as panda
import os
import mailbox
import re
import pandas

# Reading in mBox files 
# https://www.kaggle.com/datasets/wcukierski/enron-email-dataset
# https://docs.python.org/3/library/mailbox.html

# Reading the files for both the spam and non-spam (ham messages)

# Ammend these file paths for external use 
mbox_file_path = 'backend/trainingData/phishing3.mbox'
ham_file_path = 'backend/trainingData/easy_ham'
phish_file_path = 'backend/trainingData/IWSPA-AP-traindata/phish'
alien_file_path = 'backend/trainingData/alientVaultData.csv'
enron_file_path = 'backend/trainingData/enron_csv.csv'

# Read file and create mbox
def read_mbox_file():
    try:
        # Open the mbox file - this is in bytes format
        mbox = mailbox.mbox(mbox_file_path)
        print("New mbox created successfully")
        return mbox  
    except Exception as e:
        print(e)

# Files are in document type rather than mbox - https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
def read_ham_file(ham_file_path):
  content = []
  try:
    for file in os.listdir(ham_file_path):
       fileP = os.path.join(ham_file_path, file)
       with open(fileP, 'r', encoding='utf-8', errors='ignore') as file:
          contents = file.read()
          return contents 
  except Exception as e:  
     print(e)
 
  return content

def createalienVault():
    # this dataset is considerably large (67000+) , so we will take a random subset of 1% between 2022-2024
    alientList = []
    alienVaultDf = pandas.read_csv(alien_file_path)
    randomAlienVaultDf = alienVaultDf.sample(frac=0.015, random_state=1)  
    vaultDf = randomAlienVaultDf.drop(columns=['Description', 'Indicator type']) # these are irrelevant, so dropped before passed to model
    for index,rows in vaultDf.iterrows():
       alientLink = rows['Indicator']
       alientList.append(alientLink)
    return alientList

# read enron dataset - consider ethical
def read_enron_file():
   enron_list = []
   enron_df = pandas.read_csv(enron_file_path)
   for index, rows in enron_df.iterrows():
      enron_email = rows['message']
      enron_list.append(enron_email)
   return enron_list

