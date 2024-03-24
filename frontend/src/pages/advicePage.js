import React from 'react';
import '../styles/advicePage.css'


function advicePage(){
    return(
     <div className="superContainer">     
             <text>What is phishing?</text>  
                <p>Phishing is the process of fraudulently representing a legitimate entity to trick victims into revealing sensitive information. </p>
        <div className="adviceContainer">
      
           <div className="adviceLeft">
            <h1> Phishing Advice </h1>
                <div className="leftList">
                <ul>
                    <li>Dont click on suspicous links</li>
                    <li>Regulary update software</li>
                    <li>Use strong and unique passwords</li>
                    <li>Be aware of email attachments</li>
                    <li>Avoid entering personal infomation</li>
                    <li>Utilise 2-factor authentication tools</li>
                </ul>
                </div>
           </div>
           <div className="contentDivide"></div>
           <div className="adviceRight">
                <h1> Phishing Resources </h1>
                <div className="leftList">
                <ul>
                    <a href="https://business.bankofscotland.co.uk/help/online-security/suspicious-emails-texts.html#:~:text=Spotting%20a%20fake%20Bank%20of%20Scotland%20email&text=We%20never%20ask%20you%20to,messy%20layout%20and%20spelling%20mistakes.">Bank of Scotland</a>
                    <a href="https://support.microsoft.com/en-gb/windows/protect-yourself-from-phishing-0c7ea947-ba98-3bd9-7184-430e1f860a44">Microsoft Phishing Support</a>
                    <a href="https://www.strath.ac.uk/professionalservices/informationservices/cybersecurity/protectyourselffromscams/phishing/">University of Strathclyde</a>
                    <a href="https://phishing.iu.edu/tips-and-strategies/index.html">Indiana Universuty</a>
                    <a href="https://www.ncsc.gov.uk/collection/small-business-guide/avoiding-phishing-attacks">National Cyber Security Centre</a>
                    <a href="https://www.gov.uk/report-suspicious-emails-websites-phishing#:~:text=Do%20not%20give%20out%20private,not%20sure%20they're%20genuine.">Gov Uk</a>
                </ul>
                </div>
           </div>
        </div>
       
    </div>
          
    )
}

export default advicePage;