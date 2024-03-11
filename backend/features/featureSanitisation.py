import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

# comment this
def removingStopWords(content): #https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
    if content is None:
        return "No content to remove stop words"
    else:
        stopWording = set(stopwords.words('english'))
        tokenText = word_tokenize(content)
        filteredStop = ' '.join([word for word in tokenText if word.lower() not in stopWording])
        return filteredStop

def removeTags(content):
    # strip html tags for plain text - https://tutorialedge.net/python/removing-html-from-string/
    tagStrip = re.compile(r'<[^>]+>|\\n|\\|\n')
    return tagStrip.sub('', str(content))