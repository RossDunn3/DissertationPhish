import re
from readFile import read_mbox_file,read_enron_file,read_data_folder
from featureSanitisation import removing_stopwords, remove_tags
from email import message_from_string

mbox_path = 'backend/trainingData/phishing3.mbox'
ham_file_path = 'backend/trainingData/easy_ham'
phish_file_path = 'backend/trainingData/IWSPA-AP-traindata/phish'

# strip html tags for plain text - https://tutorialedge.net/python/removing-html-from-string/
# link regex - https://www.w3resource.com/python-exercises/re/python-re-exercise-42.php
link_regex = r'((http[s]?|hxxp|HXXP)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'

#Purpose: Analysis of nature of links
def extract_links(content):
    try:
        linkList_content = re.findall(link_regex, content)
        if not linkList_content:
            return None
        else:
            # can edit to return length(count of links in further analysis)
            return linkList_content   
    except TypeError:
        raise TypeError("Cannnot extract links from non-formatted input")    
    except ValueError:
        raise ValueError("Value error detected")

#Prupose: extract text content for ham files
#Searching for plain text in the email https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python
def extract_subject_content_Ham(message):
    try:
        for x in message.walk():
            if x.get_content_type() == 'text/plain': # restrcited type (need to expand)
                return x.get_payload()
    except TypeError:
       raise TypeError("Provide the correct Message input")  
    except ValueError:
        raise ValueError("Value error detected")
    except AttributeError:
        raise AttributeError("Attribute error detected: cannot apply functions to passed argument")   
      
#Prupose: extract content for mbox files
#https://stackoverflow.com/questions/7166922/extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
def extract_subject_content_Mbox(message): 
    try:
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
    except TypeError:
       raise TypeError("Provide the correct Message input")  
    except ValueError:
        raise ValueError("Value error detected")
    except AttributeError:
        raise AttributeError("Attribute error detected: cannot apply functions to passed argument")


#Purpose: extraction helper used in feature extraction functions, as well as input validation
def extraction_helper(contents):
    try:
        # each function then defines its own classifier
        msg = message_from_string(contents)
        sender = str(msg.get("From", "Unknown sender"))
        recipient = str(msg.get("To", "Unknown recipient"))
        subject = str(msg.get("Subject", "Unknown subject")).lower()
        date = str(msg.get("date", "Unknown date"))
        content_type = str(msg.get("Content-Type", "Unknown content-type"))
        content = str((extract_subject_content_Ham(msg))).lower()
        linkList_content = extract_links(content)
        sanitsed_content = removing_stopwords(remove_tags(content)) 
        content_dictionary = {  'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': content_type, 'Content': sanitsed_content, 'Links': linkList_content}
        return content_dictionary
    except TypeError:
       raise TypeError("Provide the correct Message input")  
    except AttributeError:
        raise AttributeError("Attribute error detected: cannot apply functions to passed argument")

#Purpose: function to append classifier to each dictionary
def append_helper(contents,classifier):
    try:
        content_dictionary = extraction_helper(contents)
        content_dictionary["Classifier"] = classifier
        return content_dictionary
    except TypeError:
       raise TypeError("Provide the correct Message input")  
    except AttributeError:
        raise AttributeError("Attribute error detected: cannot apply functions to passed argument")

#no limit set as less than limit files available
#Purpose: extract contents from IWSPA-V2 dataset
def extract_Phish():
    classifier = 1
    phish_list = []
    try:
        phish_contents = read_data_folder(phish_file_path)
        # https://stackoverflow.com/questions/40873284/preventing-a-python-for-loop-from-iterating-over-a-single-string-by-char
        phish_contents = phish_contents if isinstance(phish_contents, list) else [phish_contents]
        for contents in phish_contents: 
            phish_list.append(append_helper(contents,classifier))
        return phish_list
    
    except Exception as e:
        print("ERROR - ",e)    

#Purpose: extract contents from enron dataset
def extract_enron(limit=1500):
    classifier = 0
    enron_list = []
    try:
        enron_mail = read_enron_file()
        count = 0
        for message in enron_mail:
          enron_list.append(append_helper(message,classifier))
          count +=1
          if count >= limit:
             break
        return enron_list
    except Exception as e:
        print("ERROR - ", e)



# Such code has not been abstracted due to the file type of mbox
#Purpose: extract contents from mbox dataset
def extract_mbox(limit=1300): #https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python
    mboxList = []
    try:
        mbox = read_mbox_file(mbox_path)
        count = 0
        for message in mbox:
            content = (extract_subject_content_Mbox(message)).lower()
            content_type = str(message.get("Content-Type", "unknown content type")) 
            if any(ct in content_type for ct in ['text/plain', 'text/html', 'multipart/']):
                sender = str(message.get("From", "Unknown sender"))
                recipient = str(message.get("Delivered-To", "Unknown recipient"))
                subject = str(message.get("Subject", "Unkown subject")).lower()
                date = str(message.get("Date", "Unknown date"))
                content = (extract_subject_content_Mbox(message)).lower()
                linkList_content = extract_links(content)
                sanitised_content = removing_stopwords(remove_tags(content)) 
                classifier = 1 
                mbox_dictionary = {
                    'Sender' : sender, 'Recipient' : recipient, 'Subject' : subject, 'Date' : date, 'Content-Type': content_type, 'Content': sanitised_content, 'Links': linkList_content, 'Classifier': classifier
                }
                mboxList.append(mbox_dictionary)
                count += 1
           
                if count >= limit:
                    break
        return mboxList
              
    except Exception as e:
        print ("ERROR - ", e)


#Purpose: extract contents from Spamassassian dataset
def extract_ham(limit = 1800):
    count = 0
    classifier = 0
    ham_list = []
    try:
        ham_contents = read_data_folder(ham_file_path)
        # https://stackoverflow.com/questions/40873284/preventing-a-python-for-loop-from-iterating-over-a-single-string-by-char
        ham_contents = ham_contents if isinstance(ham_contents, list) else [ham_contents]
        for contents in ham_contents:
            count = count + 1 
            ham_list.append(append_helper(contents,classifier))
            if count >= limit:
                break
        return ham_list

    except Exception as e:
        print("ERROR - ", e)

