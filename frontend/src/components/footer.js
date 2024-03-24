import React from 'react';
import '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/styles/footer.css'
import { Link } from 'react-router-dom';
function footer(){
    return (
        <div className="footer">
            <div className="contact">
             <text>Contact me: </text>   
                <a href = "mailto: ross.dunn.2020@uni.strath.ac.uk">ross.dunn.2020@uni.strath.ac.uk</a>
            </div>
            
        </div>

    )
}

export default footer;