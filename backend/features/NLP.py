# apply BERT for NLP Task - https://github.com/codebasics/deep-learning-keras-tf-tutorial/blob/master/47_BERT_text_classification/BERT_email_classification-handle-imbalance.ipynb
# youtube - https://www.youtube.com/watch?v=hOCDJyZ6quA&t=616s
import pandas
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from sklearn.model_selection import train_test_split
from featureEngineering import extractDomainData
import pickle

# We only want to use the data from the subject and the email content itself - also could extract these features

# ater inclusion of domains 580s 5s/step - loss: 0.2317 - accuracy: 0.9184 - recall: 0.8492 - precision: 0.9233

def load_pickle(filename):
     with open(filename, "rb") as file:
          combined_mail = pickle.load(file)
     return combined_mail

combined_mail = load_pickle("/Users/rossdunn3/Desktop/DissertationPhish/backend/features/random_data.pkl")     

def get_language_features(mail_entry): #works in both model training and direction
   nlpList = []
   if isinstance(mail_entry, dict):
        mail_entry = [mail_entry]
   for mail in mail_entry:
        subject = str(mail["Subject"])
        content = str(mail["Content"])
        #if in training or in predicting
        if "Classifier" in mail:
            classifier = mail['Classifier']
            nlpDictionary = {"Classifier": classifier, "Subject": subject, "Content": content}
        else:
            nlpDictionary = {"Subject": subject, "Content": content}
        nlpList.append(nlpDictionary)
   nlpDataframe = pandas.DataFrame(nlpList)
   return nlpDataframe

def get_domain_features(mail_entry): # works
    domain_list = []
    if isinstance(mail_entry, dict):
         mail_entry = [mail_entry]
    domains = extractDomainData(mail_entry)
    for domain in domains:
        sender = domain["SenderDomain"]
        receiver = domain["ReceiverDomain"]
        senderCount = domain["SenderDomainCount"]
        receiverCount = domain["ReceiverDomainCount"]
        if "Classifier" in domain:
              classifier = domain['Classifier']
              domain_dictionary = {"Classifier": classifier, "SenderDomain" : sender, "ReceiverDomain" : receiver, "SenderDomainCount" : senderCount, "ReceiverDomainCount" : receiverCount}
        else:
              domain_dictionary = {"SenderDomain" : sender, "ReceiverDomain" : receiver, "SenderDomainCount" : senderCount, "ReceiverDomainCount" : receiverCount}  
        domain_list.append(domain_dictionary)
    domain_data_frame = pandas.DataFrame(domain_list)
    return domain_data_frame

# change this as domain data is already together, and just get the classifier, then train

def train_bert():
        language_df = get_language_features(combined_mail)
        domain_df = get_domain_features(combined_mail)
        #need to combine both the subject and content before passing
        language_df["Sender/Receiver"] = domain_df["SenderDomain"] + "[SEP]" + domain_df["ReceiverDomain"]
        language_df["Combination"] = language_df["Subject"] + "[SEP]" + language_df["Content"] + "[SEP]" + language_df["Sender/Receiver"]

        x_train,x_test,y_train,y_test = train_test_split(language_df["Combination"] , language_df["Classifier"], stratify=language_df['Classifier'])

        bert_preprocesser = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
        bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

        #Defining the model layers
        text_content = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        # pre processing text content
        preprocessed_text_content = bert_preprocesser(text_content)
        model_outputs = bert_encoder(preprocessed_text_content)

        #Defining NN layers
        layer =  tf.keras.layers.Dropout(0.1, name="dropout")(model_outputs['pooled_output'])
        layer = tf.keras.layers.Dense(1, activation='sigmoid', name="model_output")(layer)
        bert_model = tf.keras.Model(inputs=[text_content], outputs = [layer])


        # Analysing model performance
        # BERT metrics

        BERT_metrics = [tf.keras.metrics.BinaryAccuracy(name="accuracy"), tf.keras.metrics.Recall(name="recall"), tf.keras.metrics.Precision(name="precision")]
        bert_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=BERT_metrics)

        
        bert_model.fit(x_train,y_train, epochs=20)


        model_path = "backend/features"
        bert_model.save(model_path)

#uncomment to run model
#train_bert()