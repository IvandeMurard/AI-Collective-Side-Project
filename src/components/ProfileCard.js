import React, { useState } from 'react';
import './ProfileCard.css';

const ProfileCard = ({ profile }) => {
  const [isVideoLoaded, setIsVideoLoaded] = useState(false);

  if (!profile) return null;

  return (
    <div className="profile-card">
      <div className="video-container">
        {profile.videoUrl ? (
          <video
            src={profile.videoUrl}
            autoPlay
            muted
            loop
            playsInline
            onLoadedData={() => setIsVideoLoaded(true)}
            className={`avatar-video ${isVideoLoaded ? 'loaded' : ''}`}
          />
        ) : (
          <div className="video-placeholder">
            <div className="avatar-icon">👤</div>
            <p>No video available</p>
          </div>
        )}
        
        <div className="video-overlay">
          <div className="profile-info">
            <h3 className="name">{profile.name}</h3>
            <h4 className="project-name">{profile.project}</h4>
          </div>
        </div>
      </div>

      <div className="card-content">
        <p className="description">{profile.description}</p>
        
        {profile.tags && profile.tags.length > 0 && (
          <div className="tags">
            {profile.tags.map((tag, index) => (
              <span key={index} className="tag">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileCard;
