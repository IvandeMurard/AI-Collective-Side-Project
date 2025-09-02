"""
Example usage of the IdeaMatcher module

This file demonstrates how to use the idea_matcher module in other applications.
You can run this file directly to test the functionality with sample data.
"""

import os
from idea_matcher import IdeaMatcher, HackathonIdea, create_sample_ideas


def basic_example():
    """Basic example of using IdeaMatcher"""
    print("=== Basic IdeaMatcher Example ===\n")
    
    # Get API key (you'll need to set this)
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        print("Example: export MISTRAL_API_KEY='your-key-here'")
        return
    
    # Initialize matcher
    matcher = IdeaMatcher(api_key)
    
    # Create some sample ideas
    ideas = [
        HackathonIdea("alice", "AI-powered fitness tracker that adapts to user behavior"),
        HackathonIdea("bob", "Blockchain-based voting system for secure elections"),
        HackathonIdea("charlie", "Smart home automation using IoT sensors"),
        HackathonIdea("diana", "Mental health chatbot with personalized therapy")
    ]
    
    # New idea to match against
    new_idea = "Machine learning app for personalized nutrition recommendations"
    
    print(f"Matching: '{new_idea}'")
    print(f"Against {len(ideas)} existing ideas...\n")
    
    try:
        results = matcher.rank_ideas(ideas, new_idea)
        
        print("Results (sorted by similarity):")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['username']} ({result['similarity']}%)")
            print(f"   Idea: {result['idea']}\n")
            
    except Exception as e:
        print(f"Error: {e}")


def custom_model_example():
    """Example using a different Mistral model"""
    print("=== Custom Model Example ===\n")
    
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        return
    
    # Use a different model
    matcher = IdeaMatcher(api_key, model="mistral-small")
    
    # Use the built-in sample ideas
    sample_ideas = create_sample_ideas()
    new_idea = "Virtual reality platform for remote team collaboration"
    
    print(f"Using model: mistral-small")
    print(f"Matching: '{new_idea}'\n")
    
    try:
        results = matcher.rank_ideas(sample_ideas, new_idea)
        
        for result in results[:3]:  # Show top 3 matches
            print(f"🏆 {result['username']}: {result['similarity']}% match")
            
    except Exception as e:
        print(f"Error: {e}")


def integration_example():
    """Example of how you might integrate this into another app"""
    print("=== Integration Example ===\n")
    
    class HackathonApp:
        def __init__(self, mistral_api_key):
            self.matcher = IdeaMatcher(mistral_api_key)
            self.registered_ideas = []
        
        def register_idea(self, username, idea):
            """Register a new hackathon idea"""
            self.registered_ideas.append(HackathonIdea(username, idea))
            print(f"✅ Registered idea for {username}")
        
        def find_matches(self, new_idea, top_n=3):
            """Find top N matches for a new idea"""
            if not self.registered_ideas:
                return []
            
            results = self.matcher.rank_ideas(self.registered_ideas, new_idea)
            return results[:top_n]
        
        def suggest_collaborators(self, username, idea):
            """Suggest potential collaborators based on idea similarity"""
            # Filter out the user's own ideas
            other_ideas = [i for i in self.registered_ideas if i.username != username]
            
            if not other_ideas:
                return []
            
            matches = self.matcher.rank_ideas(other_ideas, idea)
            # Return users with >70% similarity
            return [m for m in matches if m['similarity'] > 70]
    
    # Demo the integration
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        return
    
    app = HackathonApp(api_key)
    
    # Register some ideas
    app.register_idea("alice", "AI-powered code review assistant")
    app.register_idea("bob", "Machine learning model deployment platform")
    app.register_idea("charlie", "Automated testing framework using AI")
    
    # Find matches for a new idea
    new_idea = "AI tool for debugging complex software systems"
    matches = app.find_matches(new_idea)
    
    print(f"\nTop matches for: '{new_idea}'")
    for match in matches:
        print(f"- {match['username']}: {match['similarity']}%")


if __name__ == "__main__":
    print("🚀 IdeaMatcher Examples\n")
    
    # Run all examples
    basic_example()
    print("\n" + "="*50 + "\n")
    
    custom_model_example()
    print("\n" + "="*50 + "\n")
    
    integration_example()
    
    print("\n✨ Examples completed!")
    print("To use in your own project:")
    print("from idea_matcher import IdeaMatcher, HackathonIdea")
