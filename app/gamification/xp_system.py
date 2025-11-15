"""
XP and Leveling System for German Learning Tool
Handles experience points, levels, and progression
"""

from typing import Dict, Tuple, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import XP_CONFIG, LEVEL_XP_REQUIREMENTS, CEFR_LEVEL_RANGES
from database.db_manager import get_db


class XPSystem:
    """Manages XP earning, leveling, and progression"""

    def __init__(self):
        self.db = get_db()
        self.xp_config = XP_CONFIG

    def award_xp(self, action: str, value: Optional[int] = None,
                 reason: str = "") -> Dict:
        """
        Award XP for an action

        Args:
            action: The type of action (e.g., 'vocabulary_review_correct')
            value: Optional value for actions that scale (e.g., minutes)
            reason: Human-readable reason for XP award

        Returns:
            Dict with XP details and level-up information
        """
        # Calculate XP based on action
        if action in self.xp_config:
            xp_amount = self.xp_config[action]

            # Scale XP for time-based actions
            if 'per_minute' in action and value:
                xp_amount *= value

        else:
            # Custom XP amount
            xp_amount = value if value else 0

        # Add XP to database
        result = self.db.add_xp(xp_amount, reason or action)

        # Check for achievements
        new_achievements = self.db.check_and_unlock_achievements()

        return {
            **result,
            'new_achievements': new_achievements
        }

    def get_current_level_info(self) -> Dict:
        """Get detailed information about current level"""
        stats = self.db.get_user_stats()
        current_xp = stats['total_xp']
        current_level = stats['current_level']

        # XP required for current and next level
        current_level_xp = self._get_xp_for_level(current_level)
        next_level_xp = self._get_xp_for_level(current_level + 1)

        # Progress toward next level
        xp_progress = current_xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        progress_percentage = (xp_progress / xp_needed * 100) if xp_needed > 0 else 100

        # CEFR level
        cefr_level = self._get_cefr_for_level(current_level)

        return {
            'current_level': current_level,
            'current_xp': current_xp,
            'xp_for_current_level': current_level_xp,
            'xp_for_next_level': next_level_xp,
            'xp_progress': xp_progress,
            'xp_needed_for_next': xp_needed,
            'progress_percentage': round(progress_percentage, 1),
            'cefr_level': cefr_level,
            'max_level': 70
        }

    def _get_xp_for_level(self, level: int) -> int:
        """Get XP required for a specific level"""
        if level in LEVEL_XP_REQUIREMENTS:
            return LEVEL_XP_REQUIREMENTS[level]
        # Calculate using formula for levels not in dict
        return int(100 * (level ** 1.5))

    def _get_cefr_for_level(self, level: int) -> str:
        """Get CEFR level (A1, A2, B1, B2) for a numeric level"""
        for cefr, (min_level, max_level) in CEFR_LEVEL_RANGES.items():
            if min_level <= level <= max_level:
                return cefr
        return "B2"  # Max level

    def get_level_rewards_summary(self, level: int) -> str:
        """Get a summary of what unlocks at a specific level"""
        rewards = {
            5: "Unlocked: Listening exercises",
            10: "Completed A1! Unlocked: A2 content",
            15: "Unlocked: Writing prompts (medium difficulty)",
            20: "Unlocked: Conversation scenarios (A2 level)",
            25: "Completed A2! Unlocked: B1 content",
            35: "Unlocked: Advanced grammar exercises",
            45: "Completed B1! Unlocked: B2 content",
            55: "Unlocked: Complex debate scenarios",
            70: "MAX LEVEL! You've completed B2! 🎓"
        }
        return rewards.get(level, "")

    def calculate_session_xp(self, session_data: Dict) -> Dict:
        """
        Calculate total XP for a session based on activities

        Args:
            session_data: Dict containing session activities
                {
                    'speaking_minutes': int,
                    'writing_count': int,
                    'writing_words': int,
                    'vocabulary_correct': int,
                    'vocabulary_incorrect': int,
                    'grammar_correct': int,
                    'grammar_incorrect': int,
                    'exercises_perfect': bool,
                    ...
                }
        """
        total_xp = 0
        breakdown = []

        # Speaking practice
        if session_data.get('speaking_minutes', 0) > 0:
            minutes = session_data['speaking_minutes']
            xp = minutes * self.xp_config['speaking_practice_per_minute']
            total_xp += xp
            breakdown.append(f"Speaking: {minutes} min → {xp} XP")

        # Writing exercises
        writing_count = session_data.get('writing_count', 0)
        if writing_count > 0:
            words = session_data.get('writing_words', 0)
            if words < 100:
                xp = writing_count * self.xp_config['writing_exercise_short']
            elif words < 300:
                xp = writing_count * self.xp_config['writing_exercise_medium']
            else:
                xp = writing_count * self.xp_config['writing_exercise_long']
            total_xp += xp
            breakdown.append(f"Writing: {writing_count} exercises → {xp} XP")

        # Vocabulary reviews
        vocab_correct = session_data.get('vocabulary_correct', 0)
        vocab_incorrect = session_data.get('vocabulary_incorrect', 0)
        if vocab_correct > 0:
            xp = vocab_correct * self.xp_config['vocabulary_review_correct']
            total_xp += xp
            breakdown.append(f"Vocabulary (correct): {vocab_correct} → {xp} XP")
        if vocab_incorrect > 0:
            xp = vocab_incorrect * self.xp_config['vocabulary_review_incorrect']
            total_xp += xp
            breakdown.append(f"Vocabulary (trying): {vocab_incorrect} → {xp} XP")

        # Grammar exercises
        grammar_correct = session_data.get('grammar_correct', 0)
        grammar_incorrect = session_data.get('grammar_incorrect', 0)
        if grammar_correct > 0:
            xp = grammar_correct * self.xp_config['grammar_exercise_correct']
            total_xp += xp
            breakdown.append(f"Grammar (correct): {grammar_correct} → {xp} XP")
        if grammar_incorrect > 0:
            xp = grammar_incorrect * self.xp_config['grammar_exercise_incorrect']
            total_xp += xp
            breakdown.append(f"Grammar (trying): {grammar_incorrect} → {xp} XP")

        # Login bonus (if first session of the day)
        if session_data.get('first_session_today', False):
            xp = self.xp_config['login_bonus']
            total_xp += xp
            breakdown.append(f"Daily login bonus → {xp} XP")

        # Perfect score bonus
        if session_data.get('perfect_score', False):
            bonus = int(total_xp * 0.1)  # 10% bonus
            total_xp += bonus
            breakdown.append(f"Perfect score bonus → {bonus} XP")

        return {
            'total_xp': int(total_xp),
            'breakdown': breakdown
        }


# Singleton instance
_xp_system = None

def get_xp_system() -> XPSystem:
    """Get XP system singleton"""
    global _xp_system
    if _xp_system is None:
        _xp_system = XPSystem()
    return _xp_system
