"""
Conversation Partner Module
Manages roleplay scenarios and dialogue practice
"""

from typing import Dict, List, Optional
from datetime import datetime
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import OTTO_CONFIG


# Conversation Scenarios by CEFR Level
SCENARIOS = {
    "A1": [
        {
            "id": "a1_greeting",
            "name": "Greeting and Introduction",
            "description": "Practice introducing yourself and basic greetings",
            "otto_role": "A friendly person you meet for the first time",
            "setting": "You meet someone new at a café",
            "learning_goals": ["Greetings", "Name", "Basic questions"],
            "initial_message": "Hallo! Wie heißt du?",
            "vocabulary_focus": ["Hallo", "Wie geht's", "Ich heiße", "Woher kommst du"]
        },
        {
            "id": "a1_cafe",
            "name": "Ordering at a Café",
            "description": "Order food and drinks in German",
            "otto_role": "A waiter at a German café",
            "setting": "You're at a café and want to order something",
            "learning_goals": ["Ordering", "Politeness", "Food vocabulary"],
            "initial_message": "Guten Tag! Was möchten Sie trinken?",
            "vocabulary_focus": ["Ich möchte", "bitte", "danke", "Kaffee", "Tee"]
        },
        {
            "id": "a1_shopping",
            "name": "Shopping for Food",
            "description": "Buy items at a grocery store",
            "otto_role": "A shopkeeper",
            "setting": "You're at a small grocery store",
            "learning_goals": ["Numbers", "Food items", "Polite requests"],
            "initial_message": "Guten Morgen! Wie kann ich Ihnen helfen?",
            "vocabulary_focus": ["Ich brauche", "Wie viel kostet", "Apfel", "Brot"]
        }
    ],
    "A2": [
        {
            "id": "a2_directions",
            "name": "Asking for Directions",
            "description": "Ask for and understand directions in a city",
            "otto_role": "A helpful local",
            "setting": "You're lost in Berlin and need help",
            "learning_goals": ["Direction vocabulary", "Polite questions", "Location"],
            "initial_message": "Ja, kann ich Ihnen helfen? Sie sehen verloren aus!",
            "vocabulary_focus": ["Wo ist", "geradeaus", "links", "rechts"]
        },
        {
            "id": "a2_doctor",
            "name": "At the Doctor",
            "description": "Describe symptoms and health issues",
            "otto_role": "A doctor",
            "setting": "You're at a doctor's office",
            "learning_goals": ["Body parts", "Symptoms", "Health vocabulary"],
            "initial_message": "Guten Tag! Was fehlt Ihnen heute?",
            "vocabulary_focus": ["Ich habe Schmerzen", "Kopf", "Bauch", "müde"]
        }
    ],
    "B1": [
        {
            "id": "b1_job_interview",
            "name": "Job Interview",
            "description": "Practice a simple job interview",
            "otto_role": "An interviewer at a German company",
            "setting": "You're applying for a position",
            "learning_goals": ["Professional vocabulary", "Past experiences", "Skills"],
            "initial_message": "Willkommen! Erzählen Sie mir etwas über sich.",
            "vocabulary_focus": ["Ich habe gearbeitet", "Erfahrung", "Fähigkeiten"]
        }
    ],
    "B2": [
        {
            "id": "b2_debate",
            "name": "Discussing Current Events",
            "description": "Have an opinion-based discussion",
            "otto_role": "A friend discussing news",
            "setting": "Casual discussion about a current topic",
            "learning_goals": ["Expressing opinions", "Arguments", "Complex sentences"],
            "initial_message": "Was denkst du über die aktuelle Situation?",
            "vocabulary_focus": ["Meiner Meinung nach", "Ich glaube", "Argument"]
        }
    ]
}


class ConversationManager:
    """Manages conversation practice sessions"""

    def __init__(self):
        self.scenarios = SCENARIOS
        self.current_scenario = None
        self.conversation_history = []
        self.corrections = []

    def get_scenarios_by_level(self, cefr_level: str) -> List[Dict]:
        """Get available scenarios for a CEFR level"""
        return self.scenarios.get(cefr_level, [])

    def get_all_scenarios(self) -> Dict[str, List[Dict]]:
        """Get all scenarios organized by level"""
        return self.scenarios

    def start_scenario(self, scenario_id: str, cefr_level: str) -> Dict:
        """
        Start a conversation scenario

        Returns:
            Dict with scenario info and Otto's opening message
        """
        # Find scenario
        scenarios = self.get_scenarios_by_level(cefr_level)
        scenario = next((s for s in scenarios if s['id'] == scenario_id), None)

        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found for level {cefr_level}")

        self.current_scenario = scenario
        self.conversation_history = []
        self.corrections = []

        # Add Otto's initial message to history
        otto_message = {
            'role': 'otto',
            'text': scenario['initial_message'],
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(otto_message)

        return {
            'scenario': scenario,
            'otto_message': scenario['initial_message'],
            'setting': scenario['setting'],
            'learning_goals': scenario['learning_goals']
        }

    def add_user_message(self, message: str):
        """Add user's message to conversation history"""
        user_message = {
            'role': 'user',
            'text': message,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(user_message)

    def add_otto_message(self, message: str):
        """Add Otto's response to conversation history"""
        otto_message = {
            'role': 'otto',
            'text': message,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(otto_message)

    def add_correction(self, user_text: str, corrected_text: str, explanation: str):
        """Add a grammar/vocabulary correction"""
        correction = {
            'user_text': user_text,
            'corrected_text': corrected_text,
            'explanation': explanation,
            'timestamp': datetime.now().isoformat()
        }
        self.corrections.append(correction)

    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history

    def get_corrections(self) -> List[Dict]:
        """Get all corrections made during conversation"""
        return self.corrections

    def build_conversation_prompt(self, user_message: str) -> str:
        """
        Build the prompt for the LLM to generate Otto's response

        Args:
            user_message: The user's latest message

        Returns:
            Formatted prompt for the LLM
        """
        if not self.current_scenario:
            return ""

        scenario = self.current_scenario

        # Build context
        prompt = f"""You are Otto von Lehrer, a friendly German language teacher playing the role of: {scenario['otto_role']}.

Setting: {scenario['setting']}

Your personality:
- Encouraging and patient
- Stay in character for the roleplay
- Use German appropriate for {scenario.get('cefr_level', 'A1')} level
- Keep responses natural and conversational
- If the user makes a mistake, gently correct it in your next response

Learning goals for this scenario: {', '.join(scenario['learning_goals'])}

Conversation so far:
"""

        # Add conversation history
        for msg in self.conversation_history:
            role = "Otto" if msg['role'] == 'otto' else "Student"
            prompt += f"{role}: {msg['text']}\n"

        prompt += f"Student: {user_message}\n"
        prompt += "\nOtto (respond in character, in German, keeping it simple and conversational): "

        return prompt

    def end_conversation(self) -> Dict:
        """
        End the current conversation and return summary

        Returns:
            Dict with conversation statistics
        """
        if not self.current_scenario:
            return {}

        total_messages = len(self.conversation_history)
        user_messages = len([m for m in self.conversation_history if m['role'] == 'user'])
        corrections_count = len(self.corrections)

        summary = {
            'scenario_name': self.current_scenario['name'],
            'total_messages': total_messages,
            'user_messages': user_messages,
            'corrections': corrections_count,
            'conversation_history': self.conversation_history,
            'corrections_list': self.corrections
        }

        # Reset for next conversation
        self.current_scenario = None
        self.conversation_history = []
        self.corrections = []

        return summary


# Singleton instance
_conversation_manager = None


def get_conversation_manager() -> ConversationManager:
    """Get ConversationManager singleton"""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager()
    return _conversation_manager
