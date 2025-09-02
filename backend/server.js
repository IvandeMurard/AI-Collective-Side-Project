require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from React build
app.use(express.static(path.join(__dirname, '../build')));

// API Routes
app.get('/api/profiles', (req, res) => {
  // Mock data for now - will connect to Supabase
  const mockProfiles = [
    {
      id: 1,
      name: "Alex Chen",
      project: "AI Music Generator",
      description: "Creating AI that composes personalized music",
      videoUrl: "https://example.com/video1.mp4",
      tags: ["AI", "Music", "Machine Learning"]
    },
    {
      id: 2,
      name: "Sarah Kim",
      project: "EcoTracker",
      description: "Carbon footprint tracking app",
      videoUrl: "https://example.com/video2.mp4",
      tags: ["Sustainability", "Mobile", "Environment"]
    }
  ];
  res.json(mockProfiles);
});

app.post('/api/profiles', (req, res) => {
  const { name, project, description, videoUrl, tags } = req.body;
  // TODO: Save to Supabase
  res.json({ message: 'Profile created successfully', id: Date.now() });
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build/index.html'));
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('AI Collective Avatar App - Ready for hackathon! 🚀');
});