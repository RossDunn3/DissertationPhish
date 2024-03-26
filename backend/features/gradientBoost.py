import numpy
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
from featureEncoding import collate_linkdata
from sklearn.metrics import confusion_matrix
from featureEngineering import linkData_extraction,alientVault_helper
import matplotlib.pyplot as plt
import pickle
import seaborn as sns 
from imblearn.under_sampling import RandomUnderSampler
# https://xgboost.readthedocs.io/en/stable/get_started.html

#Purpose: Loads randomised data before training
def load_pickle(filename):
     with open(filename, "rb") as file:
          combined_mail = pickle.load(file)
     return combined_mail

combined_mail = load_pickle("backend/features/random_data.pkl") 

alien = alientVault_helper()

engineering_data = linkData_extraction(combined_mail) + alien

encoding_data = collate_linkdata(engineering_data) 

#Model training code
#https://www.datacamp.com/tutorial/xgboost-in-python

#Purpose: Train XGBoost model on randomised features and display test performance via a confusion matrix
def gradientBoost_model():
    x_Data = encoding_data.drop('Classifier', axis=1)
    y_data_classifier = encoding_data['Classifier']

    X_train,X_test,y_train,y_test = train_test_split(x_Data, encoding_data['Classifier'], test_size= 0.25, stratify=encoding_data['Classifier'],random_state=42)

    binary_model = XGBClassifier(n_estimators=50 , max_depth = 4, learning_rate=0.1 , objective='binary:logistic')

    random_u_sampler = RandomUnderSampler(random_state=42, sampling_strategy='majority')

    x_fair_train, y_fair_train = random_u_sampler.fit_resample(X_train, y_train)

    binary_model.fit(x_fair_train,y_fair_train)

    binary_score = binary_model.predict(X_test)

    binary_model.save_model('backend/features/gradient_boost_model_update_weight.bin')

    confusion_diagram = confusion_matrix(y_test, binary_score)

    print(confusion_diagram)

    xgb.plot_importance(binary_model)
    plt.show()


    # https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea
    labels = ['True Neg','False Pos','False Neg','True Pos']
    labels = numpy.asarray(labels).reshape(2,2)
    sns.heatmap(confusion_diagram,annot=labels, fmt='', cmap='Blues')
    plt.savefig('backend/features/confusionUpdateWithKeyword.png', dpi=300)
    plt.close()

#uncomment to run model
gradientBoost_model()


