from flask import Flask, request, jsonify, render_template
import os
import json
from idea_matcher import IdeaMatcher, HackathonIdea
import config

app = Flask(__name__)

# Global matcher instance (will be initialized with API key)
matcher = None

def load_ideas_from_db():
    """Load ideas from the JSON database"""
    try:
        with open('ideas.json', 'r') as f:
            data = json.load(f)
            return [HackathonIdea(idea['username'], idea['idea']) for idea in data['ideas']]
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match_ideas():
    """API endpoint to match ideas using database"""
    data = request.json
    
    # Validate input - now only need new_idea
    if 'new_idea' not in data:
        return jsonify({'error': 'Missing required field: new_idea'}), 400
    
    # Load existing ideas from database
    existing_ideas = load_ideas_from_db()
    
    if len(existing_ideas) == 0:
        return jsonify({'error': 'No ideas found in database'}), 400
    
    # Get rankings (will use fallback if no API key or API fails)
    try:
        rankings = matcher.rank_ideas(existing_ideas, data['new_idea'])
        
        return jsonify({
            'new_idea': data['new_idea'],
            'rankings': rankings
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get rankings: {str(e)}'}), 500

@app.route('/api/ideas', methods=['GET'])
def get_ideas():
    """API endpoint to get all ideas from database"""
    existing_ideas = load_ideas_from_db()
    return jsonify({
        'ideas': [{'username': idea.username, 'idea': idea.idea} for idea in existing_ideas]
    })

@app.route('/api/set-api-key', methods=['POST'])
def set_api_key():
    """Set the Mistral API key"""
    global matcher
    data = request.json
    
    if 'api_key' not in data:
        return jsonify({'error': 'API key required'}), 400
    
    try:
        matcher = IdeaMatcher(data['api_key'])
        return jsonify({'message': 'API key set successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to initialize matcher: {str(e)}'}), 500

if __name__ == '__main__':
    # Try to get API key from config file first, then environment
    api_key = config.MISTRAL_API_KEY or os.getenv('MISTRAL_API_KEY')
    
    if api_key:
        try:
            matcher = IdeaMatcher(api_key, model=config.MISTRAL_MODEL, use_fallback=config.USE_RANDOM_FALLBACK)
            print("Mistral API key loaded from config/environment")
        except Exception as e:
            print(f"Failed to initialize matcher with API key: {e}")
            matcher = IdeaMatcher(use_fallback=config.USE_RANDOM_FALLBACK)
            print("Initialized matcher with fallback mode")
    else:
        matcher = IdeaMatcher(use_fallback=config.USE_RANDOM_FALLBACK)
        print("No Mistral API key found. Using fallback mode with random percentages.")
    
    app.run(debug=config.DEBUG_MODE, host=config.HOST, port=config.PORT)
