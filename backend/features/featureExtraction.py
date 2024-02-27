# Extracting features from both sets of emails
import re
import os
from readFile import read_mbox_file,read_enron_file
from featureSanitisation import removingStopWords, removeTags
from email import message_from_string


ham_file_path = 'backend/trainingData/easy_ham'
phish_file_path = 'backend/trainingData/IWSPA-AP-traindata/phish'
mbox_results = {}

#classifier have been added manually to dictionaries (0 1) to non-spam and spam respectively (is this correct)

# Need to deal with none type

# Am i going to have to parse the headers as well not just text for links, (analyse header itself??)
# Checking javascript, images?

# strip html tags for plain text - https://tutorialedge.net/python/removing-html-from-string/
tagStrip = re.compile(r'<[^>]+>|\\n|b|\\|\n')
# link regex - https://www.w3resource.com/python-exercises/re/python-re-exercise-42.php
linkRegex = r'((http[s]?|hxxp|HXXP)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'

# Analysis of nature of links
def extractLinks(content):
    linkListContent = re.findall(linkRegex, content)
    if not linkListContent:
        return None
    else:
        # can edit to return length(count of links in further analysis)
        return linkListContent   
    
# Analysis of number of links     
def linkCounter(content):
    return len(extractLinks(content))

# Searching for plain text in the email https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python
def extract_subject_content_Ham(message):
   for x in message.walk():
       if x.get_content_type() == 'text/plain': # restrcited type (need to expand)
           return x.get_payload()


def extract_subject_content_Mbox(message): #https://stackoverflow.com/questions/7166922/extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
     content = ""
     for part in message.walk():
        # Check if the part is 'text/plain' or 'text/html'
        if part.get_content_type() in ['text/plain', 'text/html']:
            charset = part.get_content_charset()
            if charset is None:
                charset = 'utf-8'  
            try:
                payload = part.get_payload(decode=True)
                content += payload.decode(charset, 'ignore')
            except LookupError:
                continue
     return content 
    
#no limit set as less than limit files available
def extract_Phish():
    phishList = []
    try:
     for file in os.listdir(phish_file_path):
        fileP = os.path.join(phish_file_path, file)
        with open(fileP, 'r', encoding='utf-8', errors='ignore') as file:
            contents = file.read()
            msg = message_from_string(contents)
            sender = str(msg.get("From", "Unknown sender"))
            recipient = str(msg.get("To", "Unknown recipient"))
            subject = str(msg.get("Subject", "Unknown subject")).lower()
            date = str(msg.get("date", "Unknown date"))
            contentType = str(msg.get("Content-Type", "Unknown content-type"))
            content = str((extract_subject_content_Ham(msg))).lower()
            linkListContent = extractLinks(content)
            sanitsedContent = removingStopWords(removeTags(content)) # this needs to be after as stop word tokenisation interferes with link regex
            classifier = 1
            phishDictionary = {
                'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': contentType, 'Content': sanitsedContent, 'Links': linkListContent, 'Classifier': classifier
            }
            phishList.append(phishDictionary)
     return phishList
    
    except Exception as e:
        print(e)    

def extract_enron(limit=1500):
    enron_list = []
    try:
        enron_mail = read_enron_file()
        count = 0
        for message in enron_mail:
            msg = message_from_string(message)
            sender = str(msg.get("From", "Unknown sender"))
            recipient = str(msg.get("To", "Unknown recipient"))
            subject = str(msg.get("Subject", "Unknown subject")).lower()
            date = str(msg.get("date", "Unknown date"))
            contentType = str(msg.get("Content-Type", "Unknown content-type"))
            content = str((extract_subject_content_Ham(msg))).lower()
            linkListContent = extractLinks(content)
            sanitsedContent = removingStopWords(removeTags(content)) # this needs to be after as stop word tokenisation interferes with link regex
            classifier = 0 
            enronDictionary = {
                'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': contentType, 'Content': sanitsedContent, 'Links': linkListContent, 'Classifier': classifier
            }
      
            enron_list.append(enronDictionary)
            count +=1
            if count >= limit:
                break

      
        return enron_list   
    except Exception as e:
        return e

def extract_mbox(limit=1300): #https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python
    mboxList = []
    try:
        mbox = read_mbox_file()
        count = 0
        for message in mbox:
            contentType = str(message.get("Content-Type", "unknown content type")) # could break
            if any(ct in contentType for ct in ['text/plain', 'text/html', 'multipart/']):
                sender = str(message.get("From", "Unknown sender"))
                recipient = str(message.get("Delivered-To", "Unknown recipient"))
                subject = str(message.get("Subject", "Unkown subject")).lower()
                date = str(message.get("Date", "Unknown date"))
                content = (extract_subject_content_Mbox(message)).lower()
                linkListContent = extractLinks(content)
                sanitisedContent = removingStopWords(removeTags(content)) # placed here as interfers with stop word removal
                classifier = 1 
                mboxDictionary = {
                    'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': contentType, 'Content': sanitisedContent, 'Links': linkListContent, 'Classifier': classifier
            }

                mboxList.append(mboxDictionary)
                count += 1
           

                if count >= limit:
                    break
            
        return mboxList
              
    except Exception as e:
        print (e)

#change this to loop over folder, it only works on one file - duplicate code from readFile.py (will ammend)
def extract_ham(limit = 1800):
    count = 0
    hamList = []
    try:
      for file in os.listdir(ham_file_path):
        fileP = os.path.join(ham_file_path, file)
        with open(fileP, 'r', encoding='utf-8', errors='ignore') as file:
            contents = file.read()
            count = count + 1 
            msg = message_from_string(contents)
            sender = str(msg.get("From", "Unknown sender"))
            recipient = str(msg.get("To", "Unknown recipient"))
            subject = str(msg.get("Subject", "Unknown subject")).lower()
            date = str(msg.get("date", "Unknown date"))
            contentType = str(msg.get("Content-Type", "Unknown content-type"))
            content = str((extract_subject_content_Ham(msg))).lower()
            linkListContent = extractLinks(content)
            sanitsedContent = removingStopWords(removeTags(content)) # this needs to be after as stop word tokenisation interferes with link regex
            classifier = 0 
            hamDictionary = {
                'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': contentType, 'Content': sanitsedContent, 'Links': linkListContent, 'Classifier': classifier
            }
      
            hamList.append(hamDictionary)

        if count >= limit:
            break

      return hamList

    except Exception as e:
        print(e)


print(extract_mbox())