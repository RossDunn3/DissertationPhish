# Implementing averged score predictions - subject to change
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import xgboost
import pandas
from featureEngineering import linkDataExtraction
from featureEncoding import collateLinkData
from NLP import get_language_features
from inputValidation import extract_content
from featureEngineering import extractDomainData
import sys

bert_path = '/Users/rossdunn3/Desktop/DissertationPhish/backend/features/bertModel'
gradientBoost_path = '/Users/rossdunn3/Desktop/DissertationPhish/backend/features/gradient_boost_model_update.bin'

bert_loaded = tf.keras.models.load_model(bert_path)
gradientBoost_loaded = xgboost.XGBClassifier()
gradientBoost_loaded.load_model(gradientBoost_path)

# So , we need to extract the same emails from the frond end inputs, and we will defer the content to each model respectively , then reach a final outcome
# email - front end input

#xgBoost model extraction 
def xgBoost_extractor(mail):
    mail_data = extract_content(mail)
    link_data = linkDataExtraction(mail_data)
    if link_data != []:
        encoded_mail = collateLinkData(link_data)
        # useless in predictions
        encoded_mail.drop(columns=["Classifier"], inplace=True)
        return gradientBoost_loaded.predict_proba(encoded_mail)[:, 1] # this right now is prediction score
    else:
       return 0 # default

# Retrieve domain data and drop numeric values as not meaningful in text semantics
def get_input_domainData(file): # works
    input_data = extract_content(file)
    domain_data = extractDomainData(input_data)
    domain_data_df = pandas.DataFrame(domain_data)
    domain_data_df.drop(columns=['SenderDomainCount'], inplace=True)
    domain_data_df.drop(columns=['ReceiverDomainCount'], inplace=True)
    return domain_data_df

# retrieve content and subject
def get_input_languageData(file):
    input_data = extract_content(file)
    language_data = get_language_features(input_data)
    return language_data

# this is predicting off single emails - change when frontend can handle >1 mail at a time
def bert_extractor(mail):
    language_df = get_input_languageData(mail)
    domain_df = get_input_domainData(mail)
    #need to combine both the subject and content before passing
    language_df["Sender/Receiver"] = domain_df["SenderDomain"] + "[SEP]" + domain_df["ReceiverDomain"]
    language_df["Combination"] = language_df["Subject"] + "[SEP]" + language_df["Content"] + "[SEP]" + language_df["Sender/Receiver"]
    # no need to encode or preproccess as this is already built into code
    combined_data = language_df["Combination"].iloc[0]
    predict = bert_loaded.predict([combined_data])
    return predict

# Combined predicton - not finalised as 0 links can contribute to legitimacy, instead of 0 score
def combined_prediction(mail):
    xgBoost_decision = xgBoost_extractor(mail)

    bert_decision = bert_extractor(mail)

    if xgBoost_decision >0: 
        final_decision = xgBoost_decision + bert_decision / 2
    else:
        final_decision = bert_decision    
  
    if final_decision > 0.6:
        print("||WARNING - This email is a phish!")
    else:
        print("||Normal email")

# calling to test
#print(combined_prediction("/Users/rossdunn3/Desktop/DissertationPhish/backend/uploads/"))

#frontend  calls    
if __name__ == "__main__":
    combined_prediction('backend/uploads')




 


                                                              





    


