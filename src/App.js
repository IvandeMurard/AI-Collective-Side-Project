import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProfileForm from './components/ProfileForm';
import SwipeScreen from './components/SwipeScreen';
import './App.css';

function App() {
  const [profiles, setProfiles] = useState([]);

  const addProfile = (profile) => {
    setProfiles([...profiles, { ...profile, id: Date.now() }]);
  };

  return (
    <Router>
      <div className="App">
        <div className="container">
          <Routes>
            <Route path="/" element={<Navigate to="/create" replace />} />
            <Route 
              path="/create" 
              element={<ProfileForm onSubmit={addProfile} />} 
            />
            <Route 
              path="/swipe" 
              element={<SwipeScreen profiles={profiles} />} 
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
