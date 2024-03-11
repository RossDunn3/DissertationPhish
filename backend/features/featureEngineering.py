# Further extraction of features from the returned dictionaries
from readFile import createalienVault
import tldextract
import ipaddress
from urllib.parse import urlparse
from phishingKeywords import list_of_keywords

#number mbox links = 1500 emails returns 2904 links
#number ham links =  1500 emails returns 1303 links
#number phish links = 629 emails returns 38 links

# ratio of nominal to phish links = 1303 : 2942

keywords = list_of_keywords()

#Sender and Receiver (Email Analysis)
def extractDomainData(mail_entries):
    try:
        domainDataList = []
        if isinstance(mail_entries, dict):
            mail_entries = [mail_entries]
        # Initially I considered the use of a dataframe but the encoding is easier when working with dictionaries
        #for each email dictionary in the list of dictionaries
        for email in mail_entries:
            senderDomain = email['Sender'].split('@')[-1]
            recieverDomain = email['Recipient'].split('@')[-1]
            senderDomainCount  = senderDomain.count('.')
            recieverDomainCount = recieverDomain.count('.')
            if 'Classifier' in email:
                emailClassifier = email['Classifier']
                domainDictionary = {'SenderDomain' : senderDomain, 'ReceiverDomain': recieverDomain, 'SenderDomainCount' : senderDomainCount,  'ReceiverDomainCount': recieverDomainCount, 'Classifier' : emailClassifier}
            else:
                domainDictionary = {'SenderDomain' : senderDomain, 'ReceiverDomain': recieverDomain, 'SenderDomainCount' : senderDomainCount,  'ReceiverDomainCount': recieverDomainCount}
            domainDataList.append(domainDictionary)

        return domainDataList
    except Exception as e:
        print("ERROR - ", e)


def alientVault_helper():
    try:
        alienLinks = []
        alienVault = createalienVault()
        classifier = 1
        for link in alienVault:
            if link is not None:
                alien_links = data_extraction(link)
                alien_links["Classifier"] = classifier
                alienLinks.append(alien_links)   
        return alienLinks
    except Exception as e:
        print("ERROR - ", e)

def data_extraction(hyperlink):
    try:
        schemeCheck = checkUrlScheme(hyperlink)
        domainExtract = tldextract.extract(hyperlink)
        domainName = domainExtract.domain
        ipCheck = checkUrlIpPresence(domainName)
        domainSubdomain = domainExtract.subdomain
        subDomainCount = len(domainSubdomain.split('.')) # subdomain counter
        lenLink = get_url_length(hyperlink)
        keyword_check = link_keywords(hyperlink)
        keyword_count = link_keywords_count(hyperlink)
        return {"Link" : hyperlink, "Scheme": schemeCheck, "IpCheck": ipCheck,"Domain": domainName, "SubDomain": domainSubdomain, "DomainSubcount": subDomainCount, "keyword" : keyword_check, "keyword_count" : keyword_count, "length": lenLink}
    except Exception as e:
        print("Error - ", e)



def linkDataExtraction(mail_entries):
    try:
        linkList = []
        # this needs to work on both a list of emails in training , as well as a single input in testing
        if isinstance(mail_entries, dict):
            mail_entries = [mail_entries]
        for mail in mail_entries:
            if "Classifier" in mail:
                classifier = mail["Classifier"]
            else:
                classifier = "Unknown"    
            linker = mail["Links"]
            if linker is not None:
                for entry in linker:
                    hyperlink = entry[0]
                    if not any(x["Link"] == hyperlink for x in linkList):
                        combinedLinkData = data_extraction(hyperlink)
                        combinedLinkData["Classifier"] = classifier
                        linkList.append(combinedLinkData)
        return linkList
    except Exception as e:
        print("ERROR - ", e)




def get_url_length(link):
    return len(link) 

def checkUrlScheme(link):
    # Lets check if the email is http or https (secure)
    try:
            linkParser = urlparse(link)
            urlScheme = linkParser.scheme
            return urlScheme
    except:
        return "no scheme for this format"    
    
#Checking the the domian name of the Link in an Ip address - return ip if true and false if not (not valid)
#https://docs.python.org/3/library/ipaddress.html
def checkUrlIpPresence(dName):
    try:
        isIpAddress = ipaddress.ip_address(dName)
        return str(isIpAddress)
    except ValueError:
        return False
    

def link_keywords(link):
    try:
        for word in keywords:
          if word.lower() in str(link).lower():
             return 1
        return 0 
    except Exception as e:
            print("ERROR - ", e)


def link_keywords_count(link):
    try:
        counter = 0
        for word in keywords:
            counter += link.lower().count(word.lower())
        return counter   
    except Exception as e:
          print("ERROR - ", e)

def printHyperLinks():
    printList = linkDataExtraction()
    for x in printList:
        print(x)
        print('\n')
    print (len(printList))

