import numpy
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from featureEncoding import collateLinkData
from featureEngineering import linkDataExtraction
from sklearn.metrics import confusion_matrix
from featureEngineering import alientVault_helper
import matplotlib.pyplot as plt
import pickle
import seaborn as sns # visualisation
# https://xgboost.readthedocs.io/en/stable/get_started.html
# accuracy = (TP + TN) / (TP + TN + FP + FN)

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

engineering_data = linkDataExtraction(combined_mail) + alien

encoding_data = collateLinkData(engineering_data)
#print(encoding_data)

linkData = encoding_data
#print(linkData)

#need to account for not having a classifier

#Data check 

def gradientBoost_model():
    xData = linkData.drop('Classifier', axis=1)
    yDataClassifier = linkData['Classifier']

    class_counts = linkData['Classifier'].value_counts()

    X_train,X_test,y_train,y_test = train_test_split(xData, linkData['Classifier'], test_size= 0.20, stratify=linkData['Classifier'],random_state=42)

    binaryModel = XGBClassifier(n_estimators=5, max_depth = 5, learning_rate=0.35 , objective='binary:logistic')
    binaryModel.fit(X_train, y_train)

    binaryScore = binaryModel.predict(X_test)

    binaryModel.save_model('backend/features/gradient_boost_model_update.bin')

    confusionMatrix = confusion_matrix(y_test, binaryScore)

    print(confusionMatrix)

    # https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea

    labels = ['True Neg','False Pos','False Neg','True Pos']
    labels = numpy.asarray(labels).reshape(2,2)
    sns.heatmap(confusionMatrix,annot=labels, fmt='', cmap='Blues')
    plt.savefig('backend/features/confusionUpdateWithKeyword.png', dpi=300)
    plt.close()

#uncomment to run model
gradientBoost_model()

# after doubling the alien vault entries, and adding the keyword count
'''
Accuracy: Approximately 84.38%. 
Precision: Approximately 91.90%. 
Recall (Sensitivity): Approximately 82.29%. 
F1 Score: Approximately 86.83%. 
'''