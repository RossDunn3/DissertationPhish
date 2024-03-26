PhishCatcher: Automating the detection of Phishing emails

A React driven website utilising natural language processing and gradient boosting algorithms to detect phishing email scams

The following text is a technical guide for the purpose of demonstration and future work:

**Step1 Pulling The Project**
Pull the project from the repo - Pull from the branch `PhishCatcher`
Link: https://github.com/RossDunn3/DissertationPhish.git

**Note**
We recommend you run this code on an IDE such as VSCode

**Step 2  File path Amendments**
Ammend the following paths to absolute paths matching that of your own machine

Right click on the local folder and click `copy path`

Replace these paths with the paths copied from your local folder:

*combinedModel*
amend both bert_path and gradientBoost_path on line 13 and 14

*inputValidation*
amend file_list on line 9

*NLP*
amend combined_mail on line 23

*Server*
amend path_to_combined on line 11

**Step3 Technology and Import setup**
Once the project is on your local machine and these file paths have been changed, you need to run a series of installs


Python3:
- Download Python: https://www.python.org/downloads/
- Run the python installer
- In the terminal, run `python3` if you are not using an IDE
- All the requirements are listed in requiremenrs.txt - run the following command to download these dependencies:
    `pip install -r requirements.txt`

React and Node js:
- Download Node js and npm: https://nodejs.org/en
- run `cd frontend` in the terminal to navigate to the react app
- Run npm install
- Run npm i
- Navigate to server.js located in `backend`
- run npm i

**STEP 4 Runnning the project**
Due to the file size contraints of Git, the bert model could not be uploaded

If you wish to run the model locally for a prediction:

-Please navigate to the file NLP and uncomment `train_bert()` on line 127:
    `cd backend/features/NLP.py`
- Please be aware this may take sometime to run

Whilst many much of the code can be run in isolation, if you wish to run the combined model for a local prediction, uncomment line 88 in `combinedModel.py`
    This will require you to insert an email into the uploads folder, as the model runs on the most recent file. This folder is in `backend/uploads`

If you wish to launch the website:
- Navigate to the react project - `cd frontend`
- Run `npm start`

If you wish to run the website and upload emails for prediction
- Navigate to the react project - `cd frontend`
- Run `npm start`
- Open a new terminal, and navigate to the backend `cd backend`
- Run `node server.js`

You are set to upload emails and receive a prediction!





