from readFile import createalienVault
import tldextract
import ipaddress
from phishingKeywords import list_of_keywords

#phishing key word list 
keywords = list_of_keywords()

#Purpose: Extact link data from a given hyperlink to be used in training
def data_extraction(hyperlink):
    try:
        domainExtract = tldextract.extract(hyperlink)
        domainName = domainExtract.domain
        ipCheck = check_url_ipPresence(domainName)
        domainSubdomain = domainExtract.subdomain
        subDomainCount = len(domainSubdomain.split('.')) # subdomain counter
        lenLink = get_url_length(hyperlink)
        keyword_check = link_keywords(hyperlink)
        keyword_count = link_keywords_count(hyperlink)
        return {"Link" : hyperlink, "IpCheck": ipCheck,"Domain": domainName, "SubDomain": domainSubdomain, "DomainSubcount": subDomainCount, "keyword" : keyword_check, "keyword_count" : keyword_count, "length": lenLink}
    except AttributeError:
        raise AttributeError("Attribute Error in data extraction function")
    



#Purpose: Sender and Receiver domain extraction from emails
def extract_domainData(mail_entries):
    try:
        domain_datalist = []
        if isinstance(mail_entries, dict):
            mail_entries = [mail_entries]
        # Initially I considered the use of a dataframe but the encoding is easier when working with dictionaries
        #for each email dictionary in the list of dictionaries
        for email in mail_entries:
            sender_domain = email['Sender'].split('@')[-1]
            reciever_domain = email['Recipient'].split('@')[-1]
  
            if 'Classifier' in email:
                email_classifier = email['Classifier']
                domain_dictionary = {'SenderDomain' : sender_domain, 'ReceiverDomain': reciever_domain, 'Classifier' : email_classifier}
            else:
                domain_dictionary = {'SenderDomain' : sender_domain, 'ReceiverDomain': reciever_domain}
            domain_datalist.append(domain_dictionary)
        return domain_datalist
    except Exception as e:
        print("ERROR - ", e)


#Purpose: Extract aline valult links from AlienOTX    
def alientVault_helper():
    try:
        alien_links_list = []
        alien_vault = createalienVault()
        classifier = 1
        for link in alien_vault:
            if link is not None:
                alien_links = data_extraction(link)
                alien_links["Classifier"] = classifier
                alien_links_list.append(alien_links)   
        return alien_links_list
    except Exception as e:
        print("ERROR - ", e)



#Purpose: Append classifier as well as extracted link data from data_extraction
def linkData_extraction(mail_entries):
    try:
        link_list = []
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
                    if not any(x["Link"] == hyperlink for x in link_list):
                        combined_linkdata = data_extraction(hyperlink)
                        combined_linkdata["Classifier"] = classifier
                        link_list.append(combined_linkdata)
        return link_list
    except Exception as e:
        print("ERROR - ", e)



#Purpose: get url length
def get_url_length(link):
    return len(link) 

    
#Purpose: Checking the the domian name of the Link in an Ip address - return ip if true and false if not (not valid)
#https://docs.python.org/3/library/ipaddress.html
def check_url_ipPresence(dName):
    try:
        is_ipAddress = ipaddress.ip_address(dName)
        return str(is_ipAddress)
    except ValueError:
        return False


#Purpose: detect keywords within hyperlink
def link_keywords(link):
    try:
        for word in keywords:
          if word.lower() in str(link).lower():
             return 1
        return 0 
    except AssertionError:
        raise AssertionError("Invalid format passed to keyword function")
    except ValueError:
        raise ValueError("Value error raised in link keyword function")


#Purpose: count keywords in hyperlink
def link_keywords_count(link):
    try:
        counter = 0
        for word in keywords:
            counter += link.lower().count(word.lower())
        return counter   
    except AttributeError:
        raise AttributeError("Invalid format passed to keyword count function")
    except ValueError:
        raise ValueError("Value error raised in link keyword count function")



