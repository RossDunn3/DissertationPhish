# when an email is passed from the front-end it needs to be altered to the format of a dictionar
from featureExtraction import message_from_string, extractLinks, removeTags, removingStopWords,extract_subject_content_Ham

# Process read file coming from frontend input
def process_txt(file):
    file_path = file
    reader = open(file_path, "r")
    content = reader.read()
    return content
    
# extracting front end content once read, utilising functions from featureExtraction (similar structure)    
def extract_content(file):
    content = process_txt(file)  
    mail_list = []
    msg = message_from_string(content)
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



