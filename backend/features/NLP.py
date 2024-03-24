import pandas
import numpy
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text # this is needed , says unused
from sklearn.model_selection import train_test_split
from featureEngineering import extract_domainData
from sklearn.metrics import confusion_matrix
import pickle
import seaborn as sns 
import matplotlib.pyplot as plt

# We only want to use the data from the subject and the email content itself - also could extract these features

# ater inclusion of domains 580s 5s/step - loss: 0.2317 - accuracy: 0.9184 - recall: 0.8492 - precision: 0.9233

#Purpose: get randomised data for model
def load_pickle(filename):
     with open(filename, "rb") as file:
          combined_mail = pickle.load(file)
     return combined_mail

combined_mail = load_pickle("/Users/rossdunn3/Desktop/DissertationPhish/backend/features/random_data.pkl")     


#Purpose: Retrieve the content subject and body from emails - If training, append classifier
def get_language_features(mail_entry): #works in both model training and direction
   try:
     nlp_list = []
     if isinstance(mail_entry, dict):
          mail_entry = [mail_entry]
     for mail in mail_entry:
          subject = str(mail["Subject"])
          content = str(mail["Content"])
          #if in training or in predicting
          if "Classifier" in mail:
               classifier = mail['Classifier']
               nlp_dictionary = {"Classifier": classifier, "Subject": subject, "Content": content}
          else:
               nlp_dictionary = {"Subject": subject, "Content": content}
          nlp_list.append(nlp_dictionary)
     nlp_dataframe = pandas.DataFrame(nlp_list)
     return nlp_dataframe
   except TypeError:
        raise TypeError("Type error in language features")
   except KeyError:
        raise KeyError("Key error in language features")
        


#Purpose: Retrieve the domain sender and receiver domains from emails - If training, append classifier
def get_domain_features(mail_entry): # works
     try:
          domain_list = []
          if isinstance(mail_entry, dict):
               mail_entry = [mail_entry]
          domains = extract_domainData(mail_entry)
          for domain in domains:
               sender = domain["SenderDomain"]
               receiver = domain["ReceiverDomain"]
               if "Classifier" in domain:
                    classifier = domain['Classifier']
                    domain_dictionary = {"Classifier": classifier, "SenderDomain" : sender, "ReceiverDomain" : receiver}
               else:
                    domain_dictionary = {"SenderDomain" : sender, "ReceiverDomain" : receiver}  
               domain_list.append(domain_dictionary)
          domain_data_frame = pandas.DataFrame(domain_list)
          return domain_data_frame
     except TypeError:
        raise TypeError("Type error in domain features")
     except KeyError:
        raise KeyError("Key error in domain features")
     

# change this as domain data is already together, and just get the classifier, then train

# apply BERT for NLP Task - https://github.com/codebasics/deep-learning-keras-tf-tutorial/blob/master/47_BERT_text_classification/BERT_email_classification-handle-imbalance.ipynb
# youtube - https://www.youtube.com/watch?v=hOCDJyZ6quA&t=616s
# https://www.analyticsvidhya.com/blog/2021/12/text-classification-using-bert-and-tensorflow/
#https://medium.com/artificialis/bert-model-for-classification-task-ham-or-spam-email-7dab2c1bd4d7
# This is the model training code used within the following train_bert function, as well as advice taken from medium article

#Purpose: training bert (natural language processing) model
def train_bert():
        language_df = get_language_features(combined_mail)
        domain_df = get_domain_features(combined_mail)
        #need to combine both the subject and content before passing
        language_df["Sender/Receiver"] = domain_df["SenderDomain"] + "[SEP]" + domain_df["ReceiverDomain"]
        language_df["Combination"] = language_df["Subject"] + "[SEP]" + language_df["Content"] + "[SEP]" + language_df["Sender/Receiver"]

        #stratify ensures equal weighting across train and test
        x_train,x_test,y_train,y_test = train_test_split(language_df["Combination"] , language_df["Classifier"], stratify=language_df['Classifier'])

        bert_preprocesser = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
        bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

        #Defining the model layers
        text_content = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        # pre processing text content
        preprocessed_text_content = bert_preprocesser(text_content)
        model_outputs = bert_encoder(preprocessed_text_content)

        #Defining NN layers
        dropout_layer =  tf.keras.layers.Dropout(0.1, name="dropout")(model_outputs['pooled_output'])
        dense_layer = tf.keras.layers.Dense(1, activation='sigmoid', name="model_output")(dropout_layer)
        bert_model = tf.keras.Model(inputs=[text_content], outputs = [dense_layer])


        # Analysing model performance
        # BERT metrics

        BERT_metrics = [tf.keras.metrics.BinaryAccuracy(name="accuracy"), tf.keras.metrics.Recall(name="recall"), tf.keras.metrics.Precision(name="precision")]
        bert_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=BERT_metrics)

        
        bert_model.fit(x_train,y_train, epochs=20)


        predict_test = bert_model.predict(x_test)
        y_prediction = (predict_test > 0.5).astype(int)
        confusion_diagram = confusion_matrix(y_test, y_prediction)
        labels = ['True Neg','False Pos','False Neg','True Pos']
        labels = numpy.asarray(labels).reshape(2,2)
        sns.heatmap(confusion_diagram,annot=labels, fmt='', cmap='YlOrRd')

        plt.savefig('backend/features/confusionBert', dpi=300)
        plt.close()


        model_path = "backend/features/bertModel"
        bert_model.save(model_path)

#uncomment to run model
#train_bert()