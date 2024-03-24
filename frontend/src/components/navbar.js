import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbar.css'
/*import { Link } from 'react-router-dom';*/

function Navbar() {
    return (
        <nav className="navbar">
                <h1>PhishCatcher</h1>
                <div className="links">
                    <Link to = "/">Home</Link>
                    <Link to = "/advice">Advice</Link>
                    <Link to = "/prediction">Prediction</Link>
       
                </div>
        </nav>

    );
}

export default Navbar;