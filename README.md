# AI Collective - Video Avatar Profile App

A mobile-first web application for presenting profiles and projects using video avatars, inspired by Tinder's swipe interface. Built for hackathons and team collaboration.

## Features

- **Profile Creation**: Simple form to create profiles with video avatars
- **Tinder-like Interface**: Swipe left/right through video profiles
- **Video Storage**: Integrated with Supabase for video hosting
- **Mobile-First Design**: Optimized for mobile devices
- **Team Collaboration**: Built for hackathon teams

## Tech Stack

- **Frontend**: React 18, React Router, Framer Motion
- **Backend**: Node.js, Express
- **Database & Storage**: Supabase
- **Styling**: CSS3 with mobile-first approach
- **Gestures**: React Spring & React Use Gesture

## Quick Start

1. **Clone and Install**
   ```bash
   git clone https://github.com/IvandeMurard/AI-Collective-Side-Project.git
   cd AI-Collective-Side-Project
   npm install
   ```

2. **Set up Supabase**
   - Create a new project at [supabase.com](https://supabase.com)
   - Copy `.env.example` to `.env`
   - Add your Supabase URL and anon key
   - Create the following table in Supabase:

   ```sql
   CREATE TABLE profiles (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     project VARCHAR(255) NOT NULL,
     description TEXT,
     video_url TEXT,
     tags TEXT[],
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

   - Create a storage bucket named `avatar-videos`

3. **Run the App**
   ```bash
   npm start
   ```

## Project Structure

```
src/
├── components/
│   ├── ProfileForm.js      # Profile creation form
│   ├── SwipeScreen.js      # Tinder-like swipe interface
│   └── ProfileCard.js      # Individual profile cards
├── services/
│   └── supabase.js         # Supabase integration
└── App.js                  # Main app with routing
```

## Usage

1. **Create Profile**: Fill out the form with your name, project details, and upload a video
2. **Browse Profiles**: Swipe right to like, left to pass
3. **Video Avatars**: Each profile features a video introduction

## Hackathon Ready

This project is designed for rapid development and deployment:
- Mobile-optimized interface
- Easy Supabase integration
- Clean, modern UI
- Team collaboration features

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for team collaboration guidelines.

## License

MIT License - Perfect for hackathon projects!
