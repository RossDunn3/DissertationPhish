# when an email is passed from the front-end it needs to be altered to the format of a dictionar
from featureExtraction import message_from_string, extractLinks, removeTags, removingStopWords,extract_subject_content_Ham
import os
import glob

# we need to get the most recent file 
# https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
def get_latest(dir):
    file_list = glob.glob('/Users/rossdunn3/Desktop/DissertationPhish/backend/uploads/1709743480749-phishing_email.txt') 
    latest_entry = max(file_list, key=os.path.getctime)  
    return latest_entry

# Process read file coming from frontend input
def process_txt(dir):
    file_path = get_latest(dir)
    reader = open(file_path, "r")
    content = reader.read()
    return content

# additonal logic intended to convert msg to eml format (outlook runs on eml)
    
# extracting front end content once read, utilising functions from featureExtraction (similar structure)    
def extract_content(file):
    content = process_txt(file)  
    mail_list = []
    msg = message_from_string(content) # this will work on txt, eml and msg from email library
    sender = str(msg.get("From", "Unknown sender"))
    recipient = str(msg.get("To", "Unknown recipient"))
    subject = str(msg.get("Subject", "Unknown subject")).lower()
    date = str(msg.get("date", "Unknown date"))
    contentType = str(msg.get("Content-Type", "Unknown content-type"))
    content = str((extract_subject_content_Ham(msg))).lower()
    linkListContent = extractLinks(content)
    sanitsedContent = removingStopWords(removeTags(content))
    file_dictionary = {
                'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': contentType, 'Content': sanitsedContent, 'Links': linkListContent,
            }
    mail_list.append(file_dictionary)
    return mail_list


