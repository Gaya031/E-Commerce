import React from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from './pages/LandingPage'
import About from './pages/About'
import Contact from './pages/Contact'
import Features from './pages/Features'
import Pricing from './pages/Pricing'
import Testimonial from './pages/Testimonial'

function App() {


  return (
    <Router>
        <Routes>
            <Route path="/" element={<LandingPage/>} />
            <Route path="/about" element={<About/>} />
            <Route path="/contact" element={<Contact/>} />
            <Route path="/features" element={<Features/>} />
            <Route path="/pricing" element={<Pricing/>} />
            <Route path="/testimonial" element={<Testimonial/>} />
        </Routes>
    </Router>
  )
}

export default App
