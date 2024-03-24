import React, {useState} from 'react';
/*import { Link } from 'react-router-dom';*/
import '../styles/predictionPage.css'
import axios from 'axios';

/*https://stackoverflow.com/questions/66736080/axios-html-show-value-on-div*/ 

/* https://www.filestack.com/fileschool/react/react-file-upload/ */
function PredictionPage() {
    const [file, setFile] = useState(null);
    const [prediction, setPrediction] = useState('')


    function handleChange(event) {
        setFile(event.target.files[0]);
    }

    function handleFile(event){
        event.preventDefault();

        if (!file) {
            alert('No file selected for upload.');
            return;
        }

        const url = "http://localhost:20502/upload";
        const formData = new FormData();
        formData.append('file', file); 
        
        alert('File uploaded successfully - Prediction in progress');

        axios.post(url, formData, {
            headers: {
                'content-type': 'multipart/form-data',
            }
         
        }).then(response => {
            console.log(response.data);
            alert('Predcition received')
            setPrediction(response.data);
            
        }).catch(error => {
            console.error('Error:', error);
            alert('File upload failed!');
        });
  
    }

    return (
        <div className="predictionContainer">
            <div className="predictionHeader">
                <text>Phishing Email Analyser</text>
            </div>
            <div class="timeMessage">
                <text>Please be aware the result may take some time to process</text>
            </div>
            <div className="fileContainer">
                <form onSubmit={handleFile}>
                   <text>Please Upload Email </text>
                    <div className="buttonContainer">
                    <input id="file" type="file" onChange={handleChange} accept=".txt, .msg, .eml"/>
                    <div className="submitContainer">
                        <button class="button" type="submit">Get Prediction</button>
                    </div>
                    </div>
                </form>
            </div>

        <div className="divider"></div>    
        <div className="verdictContainer">
            <header>Predicted result:</header>

            <div className="resultContainer" id ="prediction">{prediction}</div>  
        </div>   
        <div className="adviceContainment">
            <text>If the email was determined to be a phish, please take the necessary precautions outlined in the advice section </text>
        </div>
        </div>
    )
}

export default PredictionPage;