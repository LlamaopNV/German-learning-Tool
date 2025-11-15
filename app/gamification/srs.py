"""
Spaced Repetition System (SRS) for vocabulary review
Modified SM-2 algorithm implementation
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import SRS_CONFIG
from database.db_manager import get_db


class SpacedRepetitionSystem:
    """Manages spaced repetition for vocabulary learning"""

    def __init__(self):
        self.db = get_db()
        self.config = SRS_CONFIG

    def get_review_queue(self, limit: int = None) -> List[Dict]:
        """
        Get vocabulary words due for review

        Args:
            limit: Maximum number of words to return (uses config if None)

        Returns:
            List of vocabulary dictionaries due for review
        """
        if limit is None:
            limit = self.config['review_cards_per_day']

        due_words = self.db.get_due_reviews(limit=limit)

        # Shuffle to avoid always reviewing in same order
        random.shuffle(due_words)

        return due_words

    def get_new_words(self, cefr_level: str, limit: int = None) -> List[Dict]:
        """
        Get new vocabulary words to learn

        Args:
            cefr_level: CEFR level (A1, A2, B1, B2)
            limit: Maximum number of new words (uses config if None)

        Returns:
            List of new vocabulary words
        """
        if limit is None:
            limit = self.config['new_cards_per_day']

        # Get all words for level that haven't been seen yet
        all_words = self.db.get_vocabulary_by_level(cefr_level)
        new_words = [w for w in all_words if w['times_seen'] == 0]

        # Return limited number
        return new_words[:limit]

    def review_word(self, vocab_id: int, difficulty: str) -> Dict:
        """
        Review a word and update its SRS parameters

        Args:
            vocab_id: Vocabulary word ID
            difficulty: 'again', 'hard', 'good', 'easy'

        Returns:
            Dict with review results and next review date
        """
        # Update in database
        self.db.update_vocabulary_review(vocab_id, difficulty)

        # Get updated word info
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vocabulary WHERE id = ?", (vocab_id,))
            word = dict(cursor.fetchone())

        return {
            'word': word['word'],
            'difficulty': difficulty,
            'next_review_date': word['next_review_date'],
            'interval_days': word['interval_days'],
            'mastered': bool(word['mastered']),
            'accuracy': self._calculate_word_accuracy(word)
        }

    def _calculate_word_accuracy(self, word: Dict) -> float:
        """Calculate accuracy percentage for a word"""
        total = word['times_seen']
        if total == 0:
            return 0.0
        return round((word['times_correct'] / total) * 100, 1)

    def get_study_stats(self) -> Dict:
        """Get overall SRS study statistics"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Total reviews today
            today = datetime.now().date().isoformat()
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM vocabulary
                WHERE DATE(last_reviewed) = ?
            """, (today,))
            reviews_today = cursor.fetchone()['count']

            # Due reviews
            now = datetime.now().isoformat()
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM vocabulary
                WHERE next_review_date <= ? AND mastered = 0
            """, (now,))
            due_reviews = cursor.fetchone()['count']

            # New words available
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM vocabulary
                WHERE times_seen = 0
            """)
            new_available = cursor.fetchone()['count']

            # Mastered words
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM vocabulary
                WHERE mastered = 1
            """)
            mastered = cursor.fetchone()['count']

            # Average accuracy
            cursor.execute("""
                SELECT
                    AVG(CAST(times_correct AS FLOAT) / NULLIF(times_seen, 0)) as avg_accuracy
                FROM vocabulary
                WHERE times_seen > 0
            """)
            avg_acc = cursor.fetchone()['avg_accuracy']
            avg_accuracy = round(avg_acc * 100, 1) if avg_acc else 0

        return {
            'reviews_today': reviews_today,
            'due_reviews': due_reviews,
            'new_words_available': new_available,
            'mastered_words': mastered,
            'average_accuracy': avg_accuracy,
            'recommended_reviews': min(due_reviews, self.config['review_cards_per_day']),
            'recommended_new_words': min(new_available, self.config['new_cards_per_day'])
        }

    def get_difficult_words(self, limit: int = 10) -> List[Dict]:
        """Get words that are most difficult (low accuracy)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *,
                       CAST(times_correct AS FLOAT) / NULLIF(times_seen, 0) as accuracy
                FROM vocabulary
                WHERE times_seen >= 3
                ORDER BY accuracy ASC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_review_forecast(self, days: int = 7) -> Dict[str, int]:
        """
        Get forecast of reviews due in the next N days

        Returns:
            Dict mapping date to number of reviews due
        """
        forecast = {}
        start_date = datetime.now().date()

        for i in range(days):
            target_date = start_date + timedelta(days=i)
            target_date_str = target_date.isoformat()

            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM vocabulary
                    WHERE DATE(next_review_date) = ? AND mastered = 0
                """, (target_date_str,))
                count = cursor.fetchone()['count']

            forecast[target_date_str] = count

        return forecast

    def bulk_add_words(self, words_list: List[Dict], cefr_level: str) -> int:
        """
        Add multiple vocabulary words at once

        Args:
            words_list: List of word dictionaries
            cefr_level: CEFR level for all words

        Returns:
            Number of words added
        """
        added_count = 0
        for word_data in words_list:
            try:
                self.db.add_vocabulary(
                    word=word_data['word'],
                    translation=word_data['translation'],
                    cefr_level=cefr_level,
                    **word_data
                )
                added_count += 1
            except Exception as e:
                print(f"Error adding word {word_data.get('word')}: {e}")
                continue

        return added_count


# Singleton instance
_srs = None

def get_srs() -> SpacedRepetitionSystem:
    """Get SRS singleton"""
    global _srs
    if _srs is None:
        _srs = SpacedRepetitionSystem()
    return _srs
