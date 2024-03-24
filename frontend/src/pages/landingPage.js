import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/landingPage.css'
import phishImg from '..//13435453.png';

function landingPage() {
    return (
        <div className="landingPage">
            <div className="landingContainer">
                <div className="landingText">
                    <div className="text1"> Automated Phishing Detection</div>
                    <div className="text2"> 
                        <li href=""> Upload emails for analysis <br/></li> 
                    </div>
                    <div className="predict"> 
                        <Link to="/prediction"> Get Prediction</Link>
                    </div>
                </div>
                <img className='landingImage' src={phishImg} alt=''></img>
            </div>
            
        </div>
    )
}

export default landingPage