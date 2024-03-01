import React from 'react';
import Navbar from '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/components/navbar.js'
import '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/styles/landingPage.css'
import phishImg from '..//13435453.png';

function landingPage() {
    return (
        <div className="landingPage">
            <Navbar />
            <div className="landingContainer">
                <div className="landingText">
                    <div className="text1"> Automated Phishing Detection</div>
                    <div className="text2"> Upload emails for analysis</div>
                </div>
                <img className='landingImage' src={phishImg} alt=''></img>
            </div>
        </div>
    )
}

export default landingPage