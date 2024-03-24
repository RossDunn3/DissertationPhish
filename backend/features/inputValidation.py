# when an email is passed from the front-end it needs to be altered to the format of a dictionar
from featureExtraction import extraction_helper
import os
import glob

# we need to get the most recent file 
# https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder

def get_latest():
    file_list = glob.glob("/Users/rossdunn3/Desktop/DissertationPhish/backend/uploads/1711277347735-phishing_email.txt") 
    latest_entry = max(file_list, key=os.path.getctime)  
    return latest_entry



# Process read file coming from frontend input
def process_txt():
    file_path = get_latest()
    reader = open(file_path, "r")
    content = reader.read()
    return content

# additonal logic intended to convert msg to eml format (outlook runs on eml)
    
# extracting front end content once read, utilising functions from featureExtraction (similar structure)    
def extract_content():
    content = process_txt()  
    extract_content = extraction_helper(content)
    return extract_content
