"""
Otto von Lehrer - Your AI German Learning Buddy
Personality engine and response generation
"""

import random
from datetime import datetime, time
from typing import Dict, List, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import OTTO_CONFIG
from database.db_manager import get_db
from gamification.xp_system import get_xp_system


class OttoVonLehrer:
    """Otto von Lehrer personality and interaction manager"""

    def __init__(self):
        self.config = OTTO_CONFIG
        self.db = get_db()
        self.xp_system = get_xp_system()

    # ============================================================
    # GREETINGS
    # ============================================================

    def get_greeting(self, user_name: str = "Lernender") -> str:
        """
        Get personalized greeting based on time of day and user stats

        Args:
            user_name: User's name (default: "Lernender" = learner)

        Returns:
            Personalized greeting message
        """
        stats = self.db.get_user_stats()
        streak = self.db.get_streak_info()
        current_hour = datetime.now().hour

        # Time-based greetings
        if 5 <= current_hour < 12:
            time_greeting = "Guten Morgen"
        elif 12 <= current_hour < 18:
            time_greeting = "Guten Tag"
        elif 18 <= current_hour < 22:
            time_greeting = "Guten Abend"
        else:
            time_greeting = "Hallo"

        greeting = f"{time_greeting}! "

        # Streak celebrations
        if streak['current_streak'] >= 100:
            greeting += f"🔥 WOW! {streak['current_streak']} days! You're absolutely unstoppable!"
        elif streak['current_streak'] >= 30:
            greeting += f"🔥 {streak['current_streak']}-day streak! You're crushing it!"
        elif streak['current_streak'] >= 7:
            greeting += f"🔥 {streak['current_streak']} days in a row! Keep it up!"
        elif streak['current_streak'] >= 3:
            greeting += f"Nice! {streak['current_streak']}-day streak going!"
        else:
            # Random encouraging message
            messages = [
                "Ready to learn some German today?",
                "Let's make some progress together!",
                "Your brain is ready for German!",
                "Time to level up your German skills!",
                "Auf geht's! Let's do this!"
            ]
            greeting += random.choice(messages)

        return greeting

    # ============================================================
    # ENCOURAGEMENT & PRAISE
    # ============================================================

    def get_encouragement(self, context: str = "general") -> str:
        """
        Get encouraging message based on context

        Args:
            context: 'correct', 'incorrect', 'general', 'streak', 'level_up'

        Returns:
            Encouraging message
        """
        encouragement_map = {
            'correct': [
                "Ausgezeichnet! 🎯 Perfect!",
                "Genau richtig! ✨ Exactly right!",
                "Wunderbar! 🌟 Wonderful!",
                "Sehr gut! 👏 Very good!",
                "Fantastisch! 🎉 Fantastic!",
                "Prima! 💫 Great!",
                "Klasse! 🎊 Class!",
                "Toll! 🌈 Awesome!"
            ],
            'incorrect': [
                "Fast! Let's try that again.",
                "Gute Bemühung! Good effort!",
                "Nicht schlecht! You're getting there!",
                "Hmm, nicht ganz. Not quite, but close!",
                "Das ist okay - learning happens through mistakes!",
                "Versuch's nochmal! Try again - you've got this!"
            ],
            'general': [
                "You're doing great! Keep going! 💪",
                "I'm proud of your dedication! 🎓",
                "Every word brings you closer to fluency! 📚",
                "You're making real progress! 🚀",
                "Your consistency is paying off! ⭐"
            ],
            'streak': [
                "Your commitment is inspiring! 🔥",
                "Look at that streak! Unbelievable! 💥",
                "You're building a powerful habit! 💪",
                "Consistency is key - and you've got it! 🗝️"
            ],
            'level_up': [
                "🎉 LEVEL UP! You're growing so fast!",
                "📈 New level unlocked! Amazing progress!",
                "🌟 Congratulations on leveling up!",
                "🚀 To the next level! You're on fire!"
            ]
        }

        messages = encouragement_map.get(context, encouragement_map['general'])
        return random.choice(messages)

    # ============================================================
    # CORRECTIONS
    # ============================================================

    def format_correction(self, user_answer: str, correct_answer: str,
                         explanation: str = "", grammar_rule: str = "") -> str:
        """
        Format a gentle correction with explanation

        Args:
            user_answer: What the user said/wrote
            correct_answer: The correct answer
            explanation: Why it's incorrect
            grammar_rule: Related grammar rule

        Returns:
            Formatted correction message
        """
        correction = "💭 Almost there!\n\n"
        correction += f"You said: **{user_answer}**\n"
        correction += f"Correct: **{correct_answer}**\n\n"

        if explanation:
            correction += f"📝 {explanation}\n\n"

        if grammar_rule:
            correction += f"📚 Grammar tip: {grammar_rule}\n\n"

        correction += random.choice([
            "Don't worry - this is a tricky one! 💪",
            "You'll get it next time! 🎯",
            "Great attempt! Keep practicing! ⭐",
            "Learning from mistakes makes you stronger! 💫"
        ])

        return correction

    # ============================================================
    # SESSION FEEDBACK
    # ============================================================

    def get_session_summary(self, session_data: Dict) -> str:
        """
        Generate end-of-session summary with Otto's personality

        Args:
            session_data: Dict with session statistics

        Returns:
            Personalized session summary
        """
        duration_minutes = session_data.get('duration_seconds', 0) // 60
        xp_earned = session_data.get('xp_earned', 0)
        words_learned = session_data.get('words_learned', 0)
        accuracy = session_data.get('accuracy', 0)
        leveled_up = session_data.get('leveled_up', False)

        summary = "## 📊 Session Complete!\n\n"

        if leveled_up:
            summary += f"### 🎉 **LEVEL UP!** You're now Level {session_data['new_level']}!\n\n"

        summary += f"⏱️ **Time studied:** {duration_minutes} minutes\n"
        summary += f"⭐ **XP earned:** {xp_earned} XP\n"

        if words_learned > 0:
            summary += f"📚 **Words learned:** {words_learned} words\n"

        if accuracy > 0:
            summary += f"🎯 **Accuracy:** {accuracy}%\n"

        summary += "\n"

        # Otto's personal comment based on performance
        if accuracy >= 90:
            summary += "**Otto says:** Exzellent! Your accuracy is outstanding! You're really mastering this! 🌟\n"
        elif accuracy >= 75:
            summary += "**Otto says:** Sehr gut! You're doing really well! Keep up the great work! 💪\n"
        elif accuracy >= 60:
            summary += "**Otto says:** Gut gemacht! Good progress - you're improving with each session! 📈\n"
        else:
            summary += "**Otto says:** Don't worry about the mistakes - they're proof you're challenging yourself! Keep going! 🎯\n"

        # Motivational closer
        closers = [
            "\nSee you next time! Bis bald! 👋",
            "\nGreat work today! Tschüss! 🎓",
            "\nI'm proud of you! Bis später! ⭐",
            "\nKeep it up! Mach's gut! 🚀"
        ]
        summary += random.choice(closers)

        return summary

    # ============================================================
    # ACHIEVEMENT UNLOCKS
    # ============================================================

    def celebrate_achievement(self, achievement: Dict) -> str:
        """
        Celebrate an unlocked achievement

        Args:
            achievement: Achievement dictionary

        Returns:
            Celebration message
        """
        message = f"## 🏆 ACHIEVEMENT UNLOCKED!\n\n"
        message += f"### {achievement['icon']} {achievement['title']}\n\n"
        message += f"**{achievement['description']}**\n\n"
        message += f"*+{achievement['xp_reward']} XP!*\n\n"

        celebrations = [
            "Fantastisch! This is a big milestone! 🎉",
            "Incredible achievement! You've earned this! 🌟",
            "This is amazing! I knew you could do it! 💫",
            "Wow! You're making such great progress! 🚀",
            "Outstanding work! Keep this momentum going! 💪"
        ]

        message += random.choice(celebrations)

        return message

    # ============================================================
    # DAILY REMINDERS
    # ============================================================

    def get_daily_reminder(self) -> str:
        """Get a daily reminder/tip"""
        tips = [
            "💡 Tip: Practice a little every day - consistency beats cramming!",
            "💡 Tip: Try speaking out loud, even when alone - it builds confidence!",
            "💡 Tip: German article genders are tough - use memory tricks (e.g., der/die/das colors)!",
            "💡 Tip: Watch German shows with subtitles - it's fun learning!",
            "💡 Tip: Make mistakes boldly - they're your best teacher!",
            "💡 Tip: Keep a German journal - even 3 sentences a day helps!",
            "💡 Tip: Learn words in context, not isolation - makes them stick better!",
            "💡 Tip: Review before bed - your brain consolidates while you sleep!",
            "💡 Tip: Focus on the 1000 most common words first - they're 80% of conversations!",
            "💡 Tip: Celebrate small wins - every word learned is progress!"
        ]
        return random.choice(tips)

    # ============================================================
    # MOTIVATION
    # ============================================================

    def get_motivation_by_streak(self, streak: int) -> str:
        """Get motivational message based on current streak"""
        if streak == 0:
            return "🌱 Every journey starts with a single step. Let's begin today!"
        elif streak == 1:
            return "🌿 Great start! Come back tomorrow to build your streak!"
        elif streak == 2:
            return "🍀 Two days! You're building momentum!"
        elif streak == 6:
            return "🔥 Tomorrow makes one week! Don't break it now!"
        elif streak == 7:
            return "🎉 One full week! This is becoming a habit!"
        elif streak == 29:
            return "🚀 Tomorrow is 30 days! You're incredible!"
        elif streak == 30:
            return "👑 THIRTY DAYS! You're a learning machine!"
        elif streak == 99:
            return "💥 Tomorrow is 100 DAYS! This is legendary!"
        elif streak == 100:
            return "🏆 ONE HUNDRED DAYS! You're unstoppable! This is true dedication!"
        elif streak % 10 == 0:
            return f"⭐ {streak} days! You're an inspiration!"
        else:
            return f"💪 {streak}-day streak! Keep the fire burning!"

    # ============================================================
    # DIFFICULTY ADJUSTMENT
    # ============================================================

    def suggest_difficulty_adjustment(self, accuracy: float, current_level: str) -> Optional[str]:
        """
        Suggest difficulty adjustments based on performance

        Args:
            accuracy: Recent accuracy percentage (0-100)
            current_level: Current CEFR level

        Returns:
            Suggestion message or None
        """
        if accuracy < 50:
            return "🤔 I notice you're finding this challenging. Want to try some easier exercises first? No pressure!"
        elif accuracy > 95 and current_level != 'B2':
            return "🌟 You're crushing this level! Ready to try something more challenging?"
        else:
            return None

    # ============================================================
    # RANDOM OTTO QUOTES
    # ============================================================

    def get_random_otto_quote(self) -> str:
        """Get a random Otto quote for fun"""
        quotes = [
            "\"Remember: making mistakes in German is better than saying nothing!\" - Otto",
            "\"Every German word you learn is a key to a new conversation!\" - Otto",
            "\"The journey of a thousand words begins with 'Hallo!'\" - Otto",
            "\"Consistency is the secret ingredient to language mastery!\" - Otto",
            "\"Your accent is unique - embrace it while you improve!\" - Otto",
            "\"Grammar rules are guidelines, not prisons. Learn them, then use them!\" - Otto",
            "\"Celebrate every 'Aha!' moment - that's your brain rewiring!\" - Otto"
        ]
        return random.choice(quotes)


# Singleton instance
_otto = None

def get_otto() -> OttoVonLehrer:
    """Get Otto singleton"""
    global _otto
    if _otto is None:
        _otto = OttoVonLehrer()
    return _otto
