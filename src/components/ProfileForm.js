import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProfileForm.css';

const ProfileForm = ({ onSubmit }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    project: '',
    description: '',
    tags: '',
    videoFile: null
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      videoFile: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // TODO: Upload video to Supabase and get URL
    const videoUrl = formData.videoFile ? URL.createObjectURL(formData.videoFile) : null;
    
    const profile = {
      ...formData,
      videoUrl,
      tags: formData.tags.split(',').map(tag => tag.trim())
    };
    
    onSubmit(profile);
    navigate('/swipe');
  };

  return (
    <div className="profile-form-screen">
      <div className="header">
        <h1>Create Your Profile</h1>
        <p>Tell us about yourself and your project</p>
      </div>

      <form onSubmit={handleSubmit} className="profile-form">
        <div className="form-group">
          <label htmlFor="name">Your Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Enter your name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="project">Project Name</label>
          <input
            type="text"
            id="project"
            name="project"
            value={formData.project}
            onChange={handleInputChange}
            placeholder="Your awesome project"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Project Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Describe your project in a few sentences..."
            rows="4"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags (comma-separated)</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleInputChange}
            placeholder="AI, Web Development, Mobile"
          />
        </div>

        <div className="form-group">
          <label htmlFor="video">Avatar Video</label>
          <input
            type="file"
            id="video"
            name="video"
            accept="video/*"
            onChange={handleFileChange}
            className="file-input"
          />
          <p className="file-hint">Upload a short video introducing yourself and your project</p>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            Create Profile
          </button>
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate('/swipe')}
          >
            Skip to Browse
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProfileForm;
