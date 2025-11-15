"""
Vocabulary Learning Module
Handles vocabulary practice, review, and learning sessions
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import get_db
from gamification.srs import get_srs
from gamification.xp_system import get_xp_system
from buddy.personality import get_otto
from config import XP_CONFIG, SESSION_CONFIG


class VocabularyLearner:
    """Manages vocabulary learning sessions"""

    def __init__(self):
        self.db = get_db()
        self.srs = get_srs()
        self.xp_system = get_xp_system()
        self.otto = get_otto()

        # Session state
        self.current_session_id = None
        self.session_stats = {
            'words_learned': 0,
            'reviews_completed': 0,
            'correct_count': 0,
            'incorrect_count': 0,
            'xp_earned': 0
        }

    # ============================================================
    # SESSION MANAGEMENT
    # ============================================================

    def start_session(self, cefr_level: str = 'A1') -> Dict:
        """
        Start a new vocabulary learning session

        Args:
            cefr_level: CEFR level to practice

        Returns:
            Session info and recommendations
        """
        self.current_session_id = self.db.create_session(
            activity_type='vocabulary',
            cefr_level=cefr_level
        )

        # Reset session stats
        self.session_stats = {
            'words_learned': 0,
            'reviews_completed': 0,
            'correct_count': 0,
            'incorrect_count': 0,
            'xp_earned': 0,
            'cefr_level': cefr_level
        }

        # Get study recommendations
        srs_stats = self.srs.get_study_stats()

        return {
            'session_id': self.current_session_id,
            'greeting': self.otto.get_greeting(),
            'daily_tip': self.otto.get_daily_reminder(),
            'srs_stats': srs_stats,
            'recommendation': self._get_study_recommendation(srs_stats)
        }

    def end_session(self) -> Dict:
        """
        End the current vocabulary session

        Returns:
            Session summary with Otto's feedback
        """
        if not self.current_session_id:
            return {'error': 'No active session'}

        # Calculate accuracy
        total_reviews = self.session_stats['correct_count'] + self.session_stats['incorrect_count']
        accuracy = (self.session_stats['correct_count'] / total_reviews * 100) if total_reviews > 0 else 0

        # End session in database
        self.db.end_session(
            session_id=self.current_session_id,
            xp_earned=self.session_stats['xp_earned'],
            words_learned=self.session_stats['words_learned'],
            exercises_completed=self.session_stats['reviews_completed'],
            mistakes_made=self.session_stats['incorrect_count']
        )

        # Get level info
        level_info = self.xp_system.get_current_level_info()

        # Check for newly unlocked achievements
        new_achievements = self.db.check_and_unlock_achievements()

        # Generate Otto's summary
        session_data = {
            'duration_seconds': 0,  # Will be calculated by DB
            'xp_earned': self.session_stats['xp_earned'],
            'words_learned': self.session_stats['words_learned'],
            'accuracy': round(accuracy, 1),
            'leveled_up': False,  # TODO: Check if leveled up
            'new_level': level_info['current_level']
        }

        summary = {
            'session_stats': self.session_stats,
            'accuracy': round(accuracy, 1),
            'level_info': level_info,
            'new_achievements': new_achievements,
            'otto_summary': self.otto.get_session_summary(session_data),
            'streak_info': self.db.get_streak_info()
        }

        # Reset session
        self.current_session_id = None

        return summary

    def _get_study_recommendation(self, srs_stats: Dict) -> str:
        """Generate study recommendation based on SRS stats"""
        due_reviews = srs_stats['due_reviews']
        new_words = srs_stats['new_words_available']

        if due_reviews > 20:
            return f"📚 You have {due_reviews} words due for review! Let's start with those to keep your memory fresh."
        elif due_reviews > 0:
            return f"✨ {due_reviews} words ready to review. After that, we can learn some new ones!"
        elif new_words > 0:
            return f"🌟 Ready to learn new words? You have {new_words} waiting for you!"
        else:
            return "🎉 You're all caught up! Amazing work! Check back tomorrow for more reviews."

    # ============================================================
    # VOCABULARY REVIEW (SRS)
    # ============================================================

    def get_review_session(self, limit: int = 20) -> List[Dict]:
        """
        Get words due for review

        Args:
            limit: Maximum number of words to review

        Returns:
            List of vocabulary words to review
        """
        words = self.srs.get_review_queue(limit=limit)

        # Shuffle for variety
        random.shuffle(words)

        return words

    def review_word(self, vocab_id: int, user_answer: str,
                   difficulty: str) -> Dict:
        """
        Review a vocabulary word

        Args:
            vocab_id: ID of vocabulary word
            user_answer: User's answer (for tracking)
            difficulty: 'again', 'hard', 'good', 'easy'

        Returns:
            Review result with feedback
        """
        # Update SRS
        result = self.srs.review_word(vocab_id, difficulty)

        # Award XP
        if difficulty == 'again':
            xp_result = self.xp_system.award_xp(
                'vocabulary_review_incorrect',
                reason='Vocabulary review (trying)'
            )
            self.session_stats['incorrect_count'] += 1
            feedback = self.otto.get_encouragement('incorrect')
        else:
            xp_result = self.xp_system.award_xp(
                'vocabulary_review_correct',
                reason='Vocabulary review (correct)'
            )
            self.session_stats['correct_count'] += 1
            feedback = self.otto.get_encouragement('correct')

        # Update session stats
        self.session_stats['reviews_completed'] += 1
        self.session_stats['xp_earned'] += xp_result['xp_gained']

        return {
            'word': result['word'],
            'difficulty': difficulty,
            'next_review': result['next_review_date'],
            'interval_days': result['interval_days'],
            'mastered': result['mastered'],
            'xp_gained': xp_result['xp_gained'],
            'total_xp': xp_result['total_xp'],
            'leveled_up': xp_result['leveled_up'],
            'feedback': feedback,
            'new_achievements': xp_result.get('new_achievements', [])
        }

    # ============================================================
    # LEARN NEW WORDS
    # ============================================================

    def get_new_words(self, cefr_level: str, limit: int = 10) -> List[Dict]:
        """
        Get new words to learn

        Args:
            cefr_level: CEFR level (A1, A2, B1, B2)
            limit: Number of new words

        Returns:
            List of new vocabulary words
        """
        words = self.srs.get_new_words(cefr_level, limit=limit)
        return words

    def learn_new_word(self, vocab_id: int) -> Dict:
        """
        Mark a word as introduced/learned

        Args:
            vocab_id: Vocabulary word ID

        Returns:
            Word info and XP reward
        """
        # Mark as seen (will be scheduled for first review)
        self.srs.review_word(vocab_id, 'good')

        # Award XP for learning new word
        xp_result = self.xp_system.award_xp(
            'vocabulary_new_word',
            reason='Learned new word'
        )

        # Update session stats
        self.session_stats['words_learned'] += 1
        self.session_stats['xp_earned'] += xp_result['xp_gained']

        return {
            'xp_gained': xp_result['xp_gained'],
            'total_xp': xp_result['total_xp'],
            'leveled_up': xp_result['leveled_up'],
            'feedback': self.otto.get_encouragement('general'),
            'new_achievements': xp_result.get('new_achievements', [])
        }

    # ============================================================
    # PRACTICE MODES
    # ============================================================

    def flashcard_mode(self, words: List[Dict]) -> List[Dict]:
        """
        Prepare words for flashcard-style review

        Args:
            words: List of vocabulary words

        Returns:
            Flashcard data with front/back
        """
        flashcards = []
        for word in words:
            # Randomize direction (German->English or English->German)
            if random.choice([True, False]):
                flashcard = {
                    'id': word['id'],
                    'front': word['word'],
                    'back': word['translation'],
                    'direction': 'de_to_en',
                    'hint': word.get('part_of_speech', ''),
                    'example': word.get('example_sentence', '')
                }
            else:
                flashcard = {
                    'id': word['id'],
                    'front': word['translation'],
                    'back': word['word'],
                    'direction': 'en_to_de',
                    'hint': f"{word.get('gender', '')} ({word.get('part_of_speech', '')})",
                    'example': word.get('example_translation', '')
                }

            flashcards.append(flashcard)

        return flashcards

    def multiple_choice_mode(self, word: Dict, num_choices: int = 4) -> Dict:
        """
        Generate multiple choice question for a word

        Args:
            word: Vocabulary word
            num_choices: Number of options

        Returns:
            Multiple choice question data
        """
        # Get wrong answers from same CEFR level
        all_words = self.db.get_vocabulary_by_level(word['cefr_level'])
        wrong_answers = [w for w in all_words if w['id'] != word['id']]
        random.shuffle(wrong_answers)
        wrong_answers = wrong_answers[:num_choices - 1]

        # Create choices
        choices = [word['translation']] + [w['translation'] for w in wrong_answers]
        random.shuffle(choices)

        return {
            'question': f"What does '{word['word']}' mean?",
            'word': word['word'],
            'choices': choices,
            'correct_answer': word['translation'],
            'hint': word.get('example_sentence', ''),
            'vocab_id': word['id']
        }

    def fill_in_blank_mode(self, word: Dict) -> Dict:
        """
        Generate fill-in-the-blank exercise

        Args:
            word: Vocabulary word with example sentence

        Returns:
            Fill-in-blank question data
        """
        example = word.get('example_sentence')

        if not example or word['word'] not in example:
            return None

        # Replace word with blank
        question_text = example.replace(word['word'], '______')

        return {
            'question': question_text,
            'answer': word['word'],
            'translation': word.get('example_translation', ''),
            'vocab_id': word['id']
        }

    # ============================================================
    # STATISTICS
    # ============================================================

    def get_vocabulary_stats(self) -> Dict:
        """Get comprehensive vocabulary statistics"""
        stats = self.db.get_vocabulary_stats()
        srs_stats = self.srs.get_study_stats()
        difficult_words = self.srs.get_difficult_words(limit=5)
        forecast = self.srs.get_review_forecast(days=7)

        return {
            'total_words': stats['total_words'],
            'by_level': stats['by_level'],
            'mastered': stats['mastered'],
            'accuracy': stats['accuracy'],
            'due_reviews': srs_stats['due_reviews'],
            'new_available': srs_stats['new_words_available'],
            'reviews_today': srs_stats['reviews_today'],
            'difficult_words': difficult_words,
            'review_forecast': forecast
        }


# Singleton instance
_vocab_learner = None

def get_vocabulary_learner() -> VocabularyLearner:
    """Get VocabularyLearner singleton"""
    global _vocab_learner
    if _vocab_learner is None:
        _vocab_learner = VocabularyLearner()
    return _vocab_learner
