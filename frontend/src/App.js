import React from 'react';
import LandingPage from '../src/pages/landingPage.js';
import AdvicePage from '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/pages/advicePage.js';
import PredictionPage from './pages/predictionPage';
import Navbar from '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/components/navbar.js'
import Footer from '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/components/footer.js'
import '/Users/rossdunn3/Desktop/DissertationPhish/frontend/src/App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className='appContainer'>
      <Navbar />
      <div className='container'>
      <Routes>
          <Route path="/" element={<LandingPage/>} />
          <Route path="/advice" element={<AdvicePage/>} />
          <Route path="/prediction" element={<PredictionPage/>} />
      </Routes>
      </div>
      <Footer />
      </div>
    </Router>
  );
}

export default App;
