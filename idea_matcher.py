"""
Hackathon Idea Matcher - Core functionality for matching ideas using Mistral AI

This module provides the core functionality for analyzing and ranking hackathon ideas
based on similarity using the Mistral API. It can be easily imported and used in other applications.
"""

import requests
import json
import random
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class HackathonIdea:
    """Data structure for storing hackathon ideas with username and description"""
    username: str
    idea: str


class IdeaMatcher:
    """
    Core class for matching hackathon ideas using Mistral AI
    
    This class handles all the logic for:
    - Formatting prompts for the Mistral API
    - Making API calls to Mistral
    - Parsing and ranking responses
    - Returning structured similarity data
    """
    
    def __init__(self, mistral_api_key: str = None, model: str = "mistral-medium", use_fallback: bool = True):
        """
        Initialize the IdeaMatcher with API credentials
        
        Args:
            mistral_api_key (str): Your Mistral API key (optional)
            model (str): Mistral model to use (default: mistral-medium)
            use_fallback (bool): Use random percentages if API fails (default: True)
        """
        self.mistral_api_key = mistral_api_key
        self.model = model
        self.mistral_url = "https://api.mistral.ai/v1/chat/completions"
        self.use_fallback = use_fallback
        
    def rank_ideas(self, existing_ideas: List[HackathonIdea], new_idea: str) -> List[Dict]:
        """
        Rank existing ideas based on similarity to a new idea using Mistral API
        
        Args:
            existing_ideas (List[HackathonIdea]): List of existing ideas to compare against
            new_idea (str): The new idea to find matches for
            
        Returns:
            List[Dict]: List of dictionaries with username, idea, and similarity percentage
                       Sorted by similarity (highest first)
                       
        Raises:
            Exception: If API call fails or response cannot be parsed
        """
        if len(existing_ideas) == 0:
            return []
        
        # Try Mistral API first if key is available
        if self.mistral_api_key:
            try:
                return self._get_mistral_rankings(existing_ideas, new_idea)
            except Exception as e:
                print(f"Mistral API failed: {e}")
                if self.use_fallback:
                    print("Falling back to random percentages...")
                    return self._get_random_rankings(existing_ideas)
                else:
                    raise e
        
        # Use random fallback if no API key
        if self.use_fallback:
            print("No API key provided, using random percentages...")
            return self._get_random_rankings(existing_ideas)
        else:
            raise Exception("No Mistral API key provided and fallback disabled")
    
    def _get_mistral_rankings(self, existing_ideas: List[HackathonIdea], new_idea: str) -> List[Dict]:
        """Get rankings from Mistral API"""
        prompt = self._create_ranking_prompt(existing_ideas, new_idea)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.mistral_api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        response = requests.post(self.mistral_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        return self._parse_ranking_response(content, existing_ideas)
    
    def _get_random_rankings(self, existing_ideas: List[HackathonIdea]) -> List[Dict]:
        """Generate random similarity percentages as fallback"""
        random.seed(42)  # For consistent results
        
        results = []
        for idea in existing_ideas:
            similarity = random.randint(10, 95)  # Random percentage between 10-95
            results.append({
                'username': idea.username,
                'idea': idea.idea,
                'similarity': similarity
            })
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
    
    def _create_ranking_prompt(self, existing_ideas: List[HackathonIdea], new_idea: str) -> str:
        """
        Create a structured prompt for the Mistral API
        
        Args:
            existing_ideas (List[HackathonIdea]): Ideas to compare against
            new_idea (str): New idea for comparison
            
        Returns:
            str: Formatted prompt for Mistral API
        """
        ideas_text = ""
        for i, idea in enumerate(existing_ideas, 1):
            ideas_text += f"{i}. {idea.username}: {idea.idea}\n"
        
        prompt = f"""You are an expert at analyzing hackathon ideas and finding similarities between them.

Here are {len(existing_ideas)} existing hackathon ideas:
{ideas_text}

New idea to compare against: "{new_idea}"

Please rank each of the {len(existing_ideas)} existing ideas based on how similar they are to the new idea. Consider factors like:
- Problem domain similarity
- Technology stack overlap
- Target audience alignment
- Implementation approach similarity
- Overall concept relatedness

For each idea, provide a similarity percentage (0-100%) and respond in this exact JSON format:

[
  {{"username": "username1", "similarity": 85}},
  {{"username": "username2", "similarity": 72}},
  {{"username": "username3", "similarity": 45}}
]

Sort by similarity percentage (highest first). Only return the JSON array, no other text."""
        
        return prompt
    
    def _parse_ranking_response(self, response_content: str, existing_ideas: List[HackathonIdea]) -> List[Dict]:
        """
        Parse Mistral's response and combine with original idea data
        
        Args:
            response_content (str): Raw response from Mistral API
            existing_ideas (List[HackathonIdea]): Original ideas for reference
            
        Returns:
            List[Dict]: Parsed rankings with username, idea, and similarity
            
        Raises:
            Exception: If JSON parsing fails
        """
        try:
            # Extract JSON from response (handle potential markdown formatting)
            content = response_content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            rankings = json.loads(content)
            
            # Create a mapping of usernames to ideas
            username_to_idea = {idea.username: idea.idea for idea in existing_ideas}
            
            # Combine rankings with original ideas
            result = []
            for ranking in rankings:
                username = ranking['username']
                if username in username_to_idea:
                    result.append({
                        'username': username,
                        'idea': username_to_idea[username],
                        'similarity': ranking['similarity']
                    })
            
            return result
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Mistral response as JSON: {e}")
        except KeyError as e:
            raise Exception(f"Missing required field in response: {e}")


def create_sample_ideas() -> List[HackathonIdea]:
    """
    Create sample hackathon ideas for testing
    
    Returns:
        List[HackathonIdea]: Sample ideas for demonstration
    """
    return [
        HackathonIdea("alice", "AI-powered fitness tracker that adapts to user behavior"),
        HackathonIdea("bob", "Blockchain-based voting system for secure elections"),
        HackathonIdea("charlie", "Smart home automation using IoT sensors"),
        HackathonIdea("diana", "Mental health chatbot with personalized therapy"),
        HackathonIdea("eve", "Sustainable transportation route optimizer"),
        HackathonIdea("frank", "AR-based educational platform for STEM subjects")
    ]


# Example usage
if __name__ == "__main__":
    # This is a simple test/example of how to use the module
    import os
    
    # Get API key from environment or prompt user
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable or modify this script")
        exit(1)
    
    # Create matcher instance
    matcher = IdeaMatcher(api_key)
    
    # Create sample ideas
    sample_ideas = create_sample_ideas()
    
    # Test with a new idea
    new_idea = "Machine learning app for personalized nutrition recommendations"
    
    print(f"Matching '{new_idea}' against {len(sample_ideas)} existing ideas...")
    
    try:
        results = matcher.rank_ideas(sample_ideas, new_idea)
        
        print("\nResults:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['username']} ({result['similarity']}%): {result['idea']}")
            
    except Exception as e:
        print(f"Error: {e}")
