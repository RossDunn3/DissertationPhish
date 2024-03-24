# Implementing averged score predictions - subject to change
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import xgboost
import pandas
from featureEngineering import linkData_extraction, extract_domainData
from featureEncoding import collate_linkdata
from NLP import get_language_features
from inputValidation import extract_content
import sys

bert_path = '/Users/rossdunn3/Desktop/DissertationPhish/backend/features/bert_model_updated'
gradientBoost_path = '/Users/rossdunn3/Desktop/DissertationPhish/backend/features/gradient_boost_model_update_weight.bin'

# confusion matrix code 

bert_loaded = tf.keras.models.load_model(bert_path)
gradientBoost_loaded = xgboost.XGBClassifier()
gradientBoost_loaded.load_model(gradientBoost_path)

# So , we need to extract the same emails from the frond end inputs, and we will defer the content to each model respectively , then reach a final outcome
# email - front end input

#xgBoost model extraction 
def xgBoost_extractor():
    mail_data = extract_content()
    link_data = linkData_extraction(mail_data)
    if link_data != []:
        encoded_mail = collate_linkdata(link_data)
        # useless in predictions
        encoded_mail.drop(columns=["Classifier"], inplace=True)
        return gradientBoost_loaded.predict_proba(encoded_mail)[:, 1] # this right now is prediction score
    else:
       return 0 # default

print(xgBoost_extractor())

# Retrieve domain data and drop numeric values as not meaningful in text semantics
def get_input_domainData(): # works
    input_data = extract_content()
    domain_data = extract_domainData(input_data)
    domain_data_df = pandas.DataFrame(domain_data)
    return domain_data_df

# retrieve content and subject
def get_input_languageData():
    input_data = extract_content()
    language_data = get_language_features(input_data)
    return language_data


# this is predicting off single emails - change when frontend can handle >1 mail at a time
def bert_extractor():
    language_df = get_input_languageData()
    domain_df = get_input_domainData()
    #need to combine both the subject and content before passing
    language_df["Sender/Receiver"] = domain_df["SenderDomain"] + "[SEP]" + domain_df["ReceiverDomain"]
    language_df["Combination"] = language_df["Subject"] + "[SEP]" + language_df["Content"] + "[SEP]" + language_df["Sender/Receiver"]
    # no need to encode or preproccess as this is already built into code
    combined_data = language_df["Combination"].iloc[0]
    predict = bert_loaded.predict([combined_data])
    return predict



# Combined predicton - not finalised as 0 links can contribute to legitimacy, instead of 0 score
def combined_prediction():
    total_score = 0
    xgBoost_decision = xgBoost_extractor()
    final_xgboost_num = 0   
    bert_decision = bert_extractor()
    if isinstance(xgBoost_decision, list):
        for prediction in xgBoost_decision:
            total_score += prediction 
            final_xgboost_num = total_score / len(xgBoost_decision) 
     
    if final_xgboost_num > 0: 
        final_decision = final_xgboost_num + bert_decision / 2
    else:
        final_decision = bert_decision    
  
    if final_decision > 0.65:
        print("||WARNING - This email is a predicted phish!")
    else:
        print("||Predicted - Normal email")





#frontend  calls    
if __name__ == "__main__":
    combined_prediction()










                                                              





    


