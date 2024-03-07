import React from 'react';
import { Link } from 'react-router-dom';
import '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/styles/navbar.css'
/*import { Link } from 'react-router-dom';*/

function Navbar() {
    return (
        <nav className="navbar">
                <h1>PhishCatcher</h1>
                <div className="links">
                    <Link to = "/">Home</Link>
                    <Link to = "/advice">Advice</Link>
                    <Link to = "/prediction">Prediction</Link>
                    <Link to = "/">Profile</Link>
                </div>
        </nav>

    );
}

export default Navbar;