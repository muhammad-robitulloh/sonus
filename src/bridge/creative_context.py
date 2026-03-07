import json

class CreativeContextBridge:
    def __init__(self, brain_state):
        self.state = brain_state

    def generate_prompt_context(self, extra_data=None):
        """Format data into a prompt context for the user to pipe into Gemini."""
        context = {
            "current_project": {
                "key": self.state.get("key"),
                "bpm": self.state.get("bpm"),
                "genre": self.state.get("genre", "Melodic Dubstep/Cinematic"),
                "theme": "Odyssey / Dark Atmosphere" # Default theme
            },
            "technical_profile": extra_data or {}
        }
        
        # Simple Narrative Generation
        narrative = f"I am currently working on a {context['current_project']['genre']} project in {context['current_project']['key']} at {context['current_project']['bpm']} BPM. "
        narrative += f"The theme is {context['current_project']['theme']}. "
        
        # Example chord advice (in future, we'd extract actual chords using Music21)
        narrative += "\n--- AI ADVICE QUERY ---\n"
        narrative += "Based on my current state, what chord substitution or melodic motif could I use to increase 'emotional weight' (gravitasi)?"
        
        return {
            "json_payload": json.dumps(context, indent=4),
            "narrative_prompt": narrative
        }
