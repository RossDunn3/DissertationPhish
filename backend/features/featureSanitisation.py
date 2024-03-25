import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

#Purpose: Remove stop words from extracted email body content
def removing_stopwords(content): #https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
    try:
        if content is None:
            return "No content to remove stop words"
        else:
            stop_wording = set(stopwords.words('english'))
            token_text = word_tokenize(content)
            filtered_stop = ' '.join([word for word in token_text if word.lower() not in stop_wording])
            return filtered_stop
    except TypeError:
        raise TypeError("Invalid type passed to stopwords function")
  
#Purpose: strip identifiers and html tags from email subject content
def remove_tags(content):
    try:
        # strip html tags for plain text - https://tutorialedge.net/python/removing-html-from-string/
        tag_strip = re.compile(r'<[^>]+>|\\n|\\|\n')
        return tag_strip.sub('', str(content))
    except ValueError:
        raise ValueError("Invalid type passed to remove tags function")
    
