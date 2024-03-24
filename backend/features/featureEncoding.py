# Last step after features are extracted , they need to be encoded for model use
import pandas
from sklearn.preprocessing import LabelEncoder

# https://www.learndatasci.com/glossary/tf-idf-term-frequency-inverse-document-frequency/

# example link - {'Link': 'n', 'Scheme': '', 'IpCheck': False, 'Domain': 'n', 'SubDomain': '', 'DomainSubcount': 1, 'Classifier': 0}

# The followng code will encode each extracted feature before they are passed to they gradient boost algorithm

#Purpose: Get classifier from each mail entry
def get_classifer(link_entry):
  try:
    classifier_list = []
    for link in link_entry:
      if 'Classifier' in link:
        classifier = link['Classifier']  
        classifier_list.append(classifier)
      if not classifier_list:
        return None  
    classifier_df = pandas.DataFrame(classifier_list, columns=["Classifier"])  
    return classifier_df
  except IndexError:
    raise IndexError("Index error in classifier function")
  except TypeError:
    raise TypeError("Type error in classifier function")
  

# Purpose: Apply encoding to the links Ip check 
def encode_ip(link_entry):
  try:
    ip_list = []
    for link in link_entry:
      if link['IpCheck'] == False:
        ip_list.append(0)
      else:
        ip_list.append(1)
    ip_df = pandas.DataFrame(ip_list, columns=['Ip'])    
    return ip_df
  except IndexError:
    raise IndexError("Index error in encode IP function")
  except TypeError:
    raise TypeError("Type error in encode IP function")
  except KeyError:
    raise KeyError("Key error in encode IP function")
  
#Purpose: Abstracted function - obtains data for link length, keyword presence, keyword count and domain sub counter
def encoding_helper(link_entry, key, column):
  try:
    data_list = []
    for link in link_entry:
      if key in link:
          key_dict = link[key]
          data_list.append(key_dict)
    data_dictionary = pandas.DataFrame(data_list, columns=[column])
    return data_dictionary

  except IndexError:
    raise IndexError("Index error in encoding")
  except TypeError:
    raise TypeError("Type error in encoding")
  except KeyError:
    raise KeyError("Key error in encoding")


# Purpose: Collects all encoded data before passed to XGBoost model - stacks in position  
def collate_linkdata(link_entry): # https://stackoverflow.com/questions/53877687/how-can-i-concat-multiple-dataframes-in-python
  try:
    ip_encoding = encode_ip(link_entry)
    domainsubcounter_encoding = encoding_helper(link_entry, 'DomainSubcount', 'subDomainCount')
    keyword_presence = encoding_helper(link_entry, 'keyword', 'Keyword_Presence')
    keyword_count = encoding_helper(link_entry, 'keyword_count', 'Keyword_count')
    length = encoding_helper(link_entry, 'length', 'length')
    classifier = get_classifer(link_entry)
    list_of_link_frame = [ip_encoding,domainsubcounter_encoding,keyword_presence,keyword_count,length]
    if classifier is not None:
      list_of_link_frame.append(classifier)
    completeLinkFrame = pandas.concat(list_of_link_frame, axis=1)
    return completeLinkFrame
  except Exception as e:
    raise e

