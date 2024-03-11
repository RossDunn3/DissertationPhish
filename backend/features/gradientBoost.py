import numpy
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
from featureEncoding import collateLinkData
from featureEngineering import linkDataExtraction
from sklearn.metrics import confusion_matrix
from featureEngineering import alientVault_helper
import matplotlib.pyplot as plt
import pickle
import seaborn as sns # visualisation
from imblearn.under_sampling import RandomUnderSampler
# https://xgboost.readthedocs.io/en/stable/get_started.html
#  Note model performance once keywords added increase to 83.81% from 81.5% -  this excluded alien data 

# We only want to use the data from the subject and the email content itself - also could extract these features

def load_pickle(filename):
     with open(filename, "rb") as file:
          combined_mail = pickle.load(file)
     return combined_mail

combined_mail = load_pickle("backend/features/random_data.pkl") 

alien = alientVault_helper()

#print(combinedFrame)
# Shuffle the features of the dataframe ensuring randomness
#combinedFrame = combinedFrame.sample(frac=1).reset_index(drop=True)

# feature encoding takes a list of links from feature engineering, then gradientBoost takes a list of encoded data
#alien data currently out 
engineering_data = linkDataExtraction(combined_mail) + alien 

#print(engineering_data)

encoding_data = collateLinkData(engineering_data)

label_counts = encoding_data['Classifier'].value_counts(normalize=True)

#print(label_counts)
#print(encoding_data)

linkData = encoding_data
#print(linkData)

#need to account for not having a classifier

#Data check 


def gradientBoost_model():
    xData = linkData.drop('Classifier', axis=1)
    yDataClassifier = linkData['Classifier']

    class_counts = linkData['Classifier'].value_counts()
    # uncoment to see class counts
    #print(class_counts)
    X_train,X_test,y_train,y_test = train_test_split(xData, linkData['Classifier'], test_size= 0.20, stratify=linkData['Classifier'],random_state=42)

    binaryModel = XGBClassifier(n_estimators=50 , max_depth = 4, learning_rate=0.1 , objective='binary:logistic')

    random_u_sampler = RandomUnderSampler(random_state=42, sampling_strategy='majority')

    x_fair_train, y_fair_train = random_u_sampler.fit_resample(X_train, y_train)

    binaryModel.fit(x_fair_train,y_fair_train)

    binaryScore = binaryModel.predict(X_test)

    binaryModel.save_model('backend/features/gradient_boost_model_update.bin')

    confusionMatrix = confusion_matrix(y_test, binaryScore)

    print(confusionMatrix)

    xgb.plot_importance(binaryModel)
    plt.show()


    # https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea

    labels = ['True Neg','False Pos','False Neg','True Pos']
    labels = numpy.asarray(labels).reshape(2,2)
    sns.heatmap(confusionMatrix,annot=labels, fmt='', cmap='Blues')
    plt.savefig('backend/features/confusionUpdateWithKeyword.png', dpi=300)
    plt.close()

#uncomment to run model
#gradientBoost_model()

# after doubling the alien vault entries, and adding the keyword count
'''
before balance
 Accuracy: 83.94% - This indicates the proportion of all predictions (both positive and negative) that were correctly identified.
Recall: 80.33% - This metric shows the proportion of actual positive cases that were correctly identified, highlighting the model's ability to find all relevant instances.
Precision: 93.05% - This represents the proportion of positive identifications that were actually correct, emphasizing the model's accuracy in classifying instances as positive.
F1 Score: 86.23% - This score is a harmonic mean of precision and recall, providing a balance between them for cases where one might be more important than the other. It's particularly useful in uneven class distributions. ​​
'''