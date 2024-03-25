import pandas 
import mailbox
import os

# Reading in mBox files 
# https://www.kaggle.com/datasets/wcukierski/enron-email-dataset
# https://docs.python.org/3/library/mailbox.html

# Reading the files for both the spam and non-spam (ham messages)

mbox_file_path = 'backend/trainingData/phishing3.mbox'
phish_file_path = 'backend/trainingData/IWSPA-AP-traindata/phish'
alien_file_path = 'backend/trainingData/alientVaultData.csv'
enron_file_path = 'backend/trainingData/enron_csv.csv'
ham_file_path = 'backend/trainingData/easy_ham'


# Purpose: Read file and create mbox
def read_mbox_file(file_path):
    try:
        # Open the mbox file - this is in bytes format
        mbox = mailbox.mbox(file_path)
        return mbox
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist")
    except TypeError:
        raise TypeError("Incorrect argument type")
    except ValueError:
        raise ValueError("Incorrect value in parameter")
    except IOError:
        raise IOError("Incorrect value in parameter")



# https://remarkablemark.org/blog/2020/08/26/python-iterate-csv-rows/
# Purpose: Read alien data csv and transform to dataframe
def read_alien_data(file_path):
    try:
        alien_vault_df = pandas.read_csv(file_path)
        vault_df = alien_vault_df.drop(columns=['Description', 'Indicator type'])
        return vault_df
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist")
    except TypeError:
        raise TypeError("Incorrect argument type")
    except ValueError:
        raise ValueError("Incorrect value in parameter")
    except OSError:
        raise OSError("Incorrect value in parameter") 
    


# Purpose: This dataset is considerably large (67000+) , so we will take a random subset of 0.015% between 2022-2024
def createalienVault():
    try:
        alien_list = []
        vault_df = read_alien_data(alien_file_path)
        random_vault_df = vault_df.sample(frac=0.015, random_state=1)
        for index,rows in random_vault_df.iterrows():
            alientLink = rows['Indicator']
            alien_list.append(alientLink)
        return alien_list
    except Exception as e:
        raise e


# Purpose: Read enron corporation csv and transform to dataframe
def get_enron_file(file_path):
    try:
        enron_df = pandas.read_csv(file_path)
        return enron_df
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist")
    except ValueError:
        raise ValueError("Incorrect argument Value Passed")
    except TypeError:
        raise TypeError("Incorrect type")
    except IOError:
        raise IOError("Incorrect value in parameter") 


#Purpose: read enron dataset 
def read_enron_file():
    try:
        enron_list = []
        enron_df = get_enron_file(enron_file_path)
        for index, rows in enron_df.iterrows():
            enron_email = rows['message']
            enron_list.append(enron_email)
        return enron_list
    except Exception as e:
        raise e


#Purpose: can be used in both ham and phish datasets for folder looping and extraction
def read_data_folder(file_path):
    phish_list = []
    try:
        for file in os.listdir(file_path):
            fileP = os.path.join(file_path, file)
            with open(fileP, 'r', encoding='utf-8', errors='ignore') as file:
                contents = file.read()
                phish_list.append(contents)
        return phish_list
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist")
    except TypeError:
        raise TypeError("Incorrect type")
    except IOError:
        raise IOError("Incorrect value in parameter") 



