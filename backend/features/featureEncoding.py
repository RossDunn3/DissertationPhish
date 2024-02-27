# Last step after features are extracted , they need to be encoded for model use
from sklearn.feature_extraction import FeatureHasher
import pandas
from sklearn.preprocessing import LabelEncoder

# https://www.learndatasci.com/glossary/tf-idf-term-frequency-inverse-document-frequency/

# example link - {'Link': 'n', 'Scheme': '', 'IpCheck': False, 'Domain': 'n', 'SubDomain': '', 'DomainSubcount': 1, 'Classifier': 0}

featureHasher = FeatureHasher(n_features=200) # start with 200 (adapt)
# Apply encoding to the domains in the dictionary but not the counts or the classifier

def schemeEncoding(link_entry):
  schemeList = []
  for link in link_entry:
    if link['Scheme'] == 'https':
      schemeList.append(1)
    else:
      schemeList.append(0)  
  schemeDf = pandas.DataFrame(schemeList, columns=['SchemeHTTP'])
  return schemeDf

def get_keyword_presence(link_entry):
  keywordList = []
  for link in link_entry:
    keywordDictEntry = link['keyword']
    keywordList.append(keywordDictEntry)
  keywordDf = pandas.DataFrame(keywordList, columns=["Keyword_Presence"])
  return keywordDf  

def get_keyword_count(link_entry):
  keywordCountList = []
  for link in link_entry:
    keywordDictEntry = link['keyword_count']
    keywordCountList.append(keywordDictEntry)
  keywordCountDf = pandas.DataFrame(keywordCountList, columns=["Keyword_count"])
  return keywordCountDf  

def getListofCounts(link_entry):
  countList = []
  for link in link_entry:
    DomainSubCounter = link['DomainSubcount']
    countList.append(DomainSubCounter)
  countDf = pandas.DataFrame(countList, columns=["subDomainCount"])  
  return countDf

def getClassifer(link_entry):
  classifierList = []
  for link in link_entry:
    if 'Classifier' in link:
      classifier = link['Classifier']  # needs to be adjusted for live purpose
      classifierList.append(classifier)
    if not classifierList:
      return None  
  classifierDf = pandas.DataFrame(classifierList, columns=["Classifier"])  
  return classifierDf
  
def encodeLinkDomains(link_entry): 
  labelEncoder = LabelEncoder()
  encodedDomainsList = []
  encodedSubDomainsList = []
  for link in link_entry:
    domainsDictEntry = link['Domain']
    subDomainsDictEntry = link['SubDomain']
    encodedDomainsList.append(domainsDictEntry)
    encodedSubDomainsList.append(subDomainsDictEntry)
  hashedLinkDomains = labelEncoder.fit_transform(encodedDomainsList)
  hashedSubDomains = labelEncoder.fit_transform(encodedSubDomainsList)
  hashLinkDf = pandas.DataFrame(hashedLinkDomains, columns=["domain"])
  hashSubDomainDf = pandas.DataFrame(hashedSubDomains, columns=["subdomain"])
  return hashLinkDf,hashSubDomainDf

# Apply encoding to the links Ip check 
def encodeIp(link_entry):
  ipList = []
  for link in link_entry:
    if link['IpCheck'] == False:
      ipList.append(0)
    else:
      ipList.append(1)
  ipDf = pandas.DataFrame(ipList, columns=['Ip'])    
  return ipDf


# having problems with data type of dataframe in model, encoding entire list should fix it    
def collateLinkData(link_entry): # https://stackoverflow.com/questions/53877687/how-can-i-concat-multiple-dataframes-in-python
  hyperlinkSchemeEncoding = schemeEncoding(link_entry)
  ipEncoding = encodeIp(link_entry)
  domainEncoding = encodeLinkDomains(link_entry)[0]
  subDomainEncoding = encodeLinkDomains(link_entry)[1]
  domainSubCounterEncoding = getListofCounts(link_entry)
  keywordPresence = get_keyword_presence(link_entry)
  keyword_count = get_keyword_count(link_entry)
  classifier = getClassifer(link_entry)
  listOfLinkFrame = [hyperlinkSchemeEncoding,ipEncoding,domainEncoding,subDomainEncoding,domainSubCounterEncoding,keywordPresence,keyword_count]
  if classifier is not None:
    listOfLinkFrame.append(classifier)
  completeLinkFrame = pandas.concat(listOfLinkFrame, axis=1)
  return completeLinkFrame

#enron dataset adds an extra 637 links to the dataset , from 1302 to 1939 - that is at an enron count of 1500




