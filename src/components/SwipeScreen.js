import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import { useDrag } from 'react-use-gesture';
import ProfileCard from './ProfileCard';
import './SwipeScreen.css';

const SwipeScreen = ({ profiles }) => {
  const navigate = useNavigate();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [allProfiles, setAllProfiles] = useState([]);

  useEffect(() => {
    // Fetch profiles from API
    const fetchProfiles = async () => {
      try {
        const response = await fetch('/api/profiles');
        const apiProfiles = await response.json();
        setAllProfiles([...profiles, ...apiProfiles]);
      } catch (error) {
        console.error('Error fetching profiles:', error);
        setAllProfiles(profiles);
      }
    };
    
    fetchProfiles();
  }, [profiles]);

  const [{ x, y, rotation }, set] = useSpring(() => ({ 
    x: 0, 
    y: 0, 
    rotation: 0 
  }));

  const bind = useDrag(({ down, movement: [mx, my], direction: [xDir], velocity }) => {
    const trigger = velocity > 0.2;
    const dir = xDir < 0 ? -1 : 1;
    
    if (!down && trigger) {
      // Swipe action
      if (dir === 1) {
        handleLike();
      } else {
        handleReject();
      }
    }
    
    set({ 
      x: down ? mx : 0, 
      y: down ? my : 0,
      rotation: down ? mx / 10 : 0
    });
  });

  const handleLike = () => {
    console.log('Liked:', allProfiles[currentIndex]);
    nextProfile();
  };

  const handleReject = () => {
    console.log('Rejected:', allProfiles[currentIndex]);
    nextProfile();
  };

  const nextProfile = () => {
    if (currentIndex < allProfiles.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // No more profiles
      setCurrentIndex(0);
    }
  };

  const currentProfile = allProfiles[currentIndex];

  if (allProfiles.length === 0) {
    return (
      <div className="swipe-screen">
        <div className="empty-state">
          <h2>No Profiles Yet</h2>
          <p>Create your profile first or wait for others to join!</p>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/create')}
          >
            Create Profile
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="swipe-screen">
      <div className="header">
        <button 
          className="back-btn"
          onClick={() => navigate('/create')}
        >
          ← Back
        </button>
        <h2>Discover Projects</h2>
        <div className="counter">
          {currentIndex + 1} / {allProfiles.length}
        </div>
      </div>

      <div className="swipe-container">
        <animated.div
          {...bind()}
          style={{
            x,
            y,
            rotation,
            touchAction: 'none'
          }}
          className="swipe-card"
        >
          <ProfileCard profile={currentProfile} />
        </animated.div>
      </div>

      <div className="action-buttons">
        <button 
          className="action-btn reject-btn"
          onClick={handleReject}
        >
          ✕
        </button>
        <button 
          className="action-btn like-btn"
          onClick={handleLike}
        >
          ♥
        </button>
      </div>
    </div>
  );
};

export default SwipeScreen;
