"""
Database Manager for German Learning Tool
Handles all database operations with SQLite
"""

import sqlite3
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from contextlib import contextmanager
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import DATABASE_PATH

class DatabaseManager:
    """Manages all database operations for the German Learning Tool"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.initialize_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def initialize_database(self):
        """Initialize database with schema if it doesn't exist"""
        schema_path = Path(__file__).parent / "schema.sql"

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)

    # ============================================================
    # USER STATS
    # ============================================================

    def get_user_stats(self) -> Dict[str, Any]:
        """Get current user statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_stats WHERE id = 1")
            row = cursor.fetchone()
            return dict(row) if row else self._create_default_user_stats()

    def _create_default_user_stats(self) -> Dict[str, Any]:
        """Create default user stats if none exist"""
        default_stats = {
            'id': 1,
            'total_xp': 0,
            'current_level': 1,
            'streak_days': 0,
            'longest_streak': 0,
            'last_activity_date': None,
            'total_seconds_studied': 0,
            'current_cefr_level': 'A1',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_stats
                (id, current_cefr_level, created_at, updated_at)
                VALUES (1, 'A1', ?, ?)
            """, (default_stats['created_at'], default_stats['updated_at']))

        return default_stats

    def update_user_stats(self, **kwargs):
        """Update user statistics"""
        kwargs['updated_at'] = datetime.now().isoformat()

        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values())

        with self.get_connection() as conn:
            conn.execute(f"""
                UPDATE user_stats
                SET {set_clause}
                WHERE id = 1
            """, values)

    def add_xp(self, xp: int, reason: str = "") -> Dict[str, Any]:
        """Add XP and check for level up"""
        stats = self.get_user_stats()
        old_level = stats['current_level']
        new_xp = stats['total_xp'] + xp

        # Calculate new level based on XP
        new_level = self._calculate_level(new_xp)

        self.update_user_stats(
            total_xp=new_xp,
            current_level=new_level
        )

        return {
            'xp_gained': xp,
            'total_xp': new_xp,
            'old_level': old_level,
            'new_level': new_level,
            'leveled_up': new_level > old_level,
            'reason': reason
        }

    def _calculate_level(self, xp: int) -> int:
        """Calculate level based on XP using formula: 100 * N^1.5"""
        level = 1
        while True:
            required_xp = int(100 * (level ** 1.5))
            if xp < required_xp:
                return level - 1 if level > 1 else 1
            level += 1
            if level > 70:  # Max level
                return 70

    # ============================================================
    # VOCABULARY
    # ============================================================

    def add_vocabulary(self, word: str, translation: str, cefr_level: str,
                      **kwargs) -> int:
        """Add a new vocabulary word"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO vocabulary
                (word, translation, cefr_level, part_of_speech, gender,
                 plural_form, example_sentence, example_translation,
                 source, created_at, next_review_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                word, translation, cefr_level,
                kwargs.get('part_of_speech'),
                kwargs.get('gender'),
                kwargs.get('plural_form'),
                kwargs.get('example_sentence'),
                kwargs.get('example_translation'),
                kwargs.get('source'),
                datetime.now().isoformat(),
                datetime.now().isoformat()  # Review immediately for new words
            ))
            return cursor.lastrowid

    def get_vocabulary_by_level(self, cefr_level: str) -> List[Dict]:
        """Get all vocabulary for a specific CEFR level"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM vocabulary
                WHERE cefr_level = ?
                ORDER BY created_at DESC
            """, (cefr_level,))
            return [dict(row) for row in cursor.fetchall()]

    def get_due_reviews(self, limit: int = 20) -> List[Dict]:
        """Get vocabulary words due for review (SRS)"""
        now = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM vocabulary
                WHERE next_review_date <= ?
                AND mastered = 0
                ORDER BY next_review_date ASC
                LIMIT ?
            """, (now, limit))
            return [dict(row) for row in cursor.fetchall()]

    def update_vocabulary_review(self, vocab_id: int, difficulty: str):
        """
        Update vocabulary after review using SM-2 algorithm
        difficulty: 'again', 'hard', 'good', 'easy'
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vocabulary WHERE id = ?", (vocab_id,))
            vocab = dict(cursor.fetchone())

            # Update review stats
            times_seen = vocab['times_seen'] + 1
            ease_factor = vocab['ease_factor']
            interval = vocab['interval_days']
            repetitions = vocab['repetitions']

            if difficulty == 'again':
                times_incorrect = vocab['times_incorrect'] + 1
                repetitions = 0
                interval = 1
                ease_factor = max(1.3, ease_factor - 0.2)
            elif difficulty == 'hard':
                times_correct = vocab['times_correct'] + 1
                ease_factor = max(1.3, ease_factor - 0.15)
                interval = max(1, int(interval * 1.2))
                repetitions += 1
            elif difficulty == 'good':
                times_correct = vocab['times_correct'] + 1
                interval = int(interval * ease_factor) if repetitions > 0 else 1
                repetitions += 1
            elif difficulty == 'easy':
                times_correct = vocab['times_correct'] + 1
                ease_factor = min(2.5, ease_factor + 0.15)
                interval = int(interval * ease_factor * 1.3) if repetitions > 0 else 3
                repetitions += 1

            # Calculate next review date
            next_review = datetime.now() + timedelta(days=interval)

            # Check if mastered (interval > 21 days)
            mastered = 1 if interval > 21 else 0

            # Update database
            cursor.execute("""
                UPDATE vocabulary
                SET times_seen = ?, times_correct = ?, times_incorrect = ?,
                    ease_factor = ?, interval_days = ?, repetitions = ?,
                    last_reviewed = ?, next_review_date = ?, mastered = ?
                WHERE id = ?
            """, (
                times_seen,
                times_correct if difficulty != 'again' else vocab['times_correct'],
                times_incorrect if difficulty == 'again' else vocab['times_incorrect'],
                ease_factor, interval, repetitions,
                datetime.now().isoformat(), next_review.isoformat(), mastered,
                vocab_id
            ))

    def get_vocabulary_stats(self) -> Dict[str, Any]:
        """Get vocabulary statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total words
            cursor.execute("SELECT COUNT(*) as total FROM vocabulary")
            total = cursor.fetchone()['total']

            # By level
            cursor.execute("""
                SELECT cefr_level, COUNT(*) as count
                FROM vocabulary
                GROUP BY cefr_level
            """)
            by_level = {row['cefr_level']: row['count'] for row in cursor.fetchall()}

            # Mastered
            cursor.execute("SELECT COUNT(*) as mastered FROM vocabulary WHERE mastered = 1")
            mastered = cursor.fetchone()['mastered']

            # Accuracy
            cursor.execute("""
                SELECT
                    SUM(times_correct) as correct,
                    SUM(times_seen) as total_reviews
                FROM vocabulary
            """)
            acc = cursor.fetchone()
            accuracy = (acc['correct'] / acc['total_reviews'] * 100) if acc['total_reviews'] > 0 else 0

            return {
                'total_words': total,
                'by_level': by_level,
                'mastered': mastered,
                'accuracy': round(accuracy, 2)
            }

    # ============================================================
    # SESSIONS
    # ============================================================

    def create_session(self, activity_type: str, cefr_level: str = None) -> int:
        """Create a new learning session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (start_time, activity_type, cefr_level)
                VALUES (?, ?, ?)
            """, (datetime.now().isoformat(), activity_type, cefr_level))
            return cursor.lastrowid

    def end_session(self, session_id: int, xp_earned: int = 0,
                   words_learned: int = 0, exercises_completed: int = 0,
                   mistakes_made: int = 0, notes: str = ""):
        """End a session and update stats"""
        end_time = datetime.now()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get session start time
            cursor.execute("SELECT start_time FROM sessions WHERE id = ?", (session_id,))
            start_time = datetime.fromisoformat(cursor.fetchone()['start_time'])

            duration_seconds = int((end_time - start_time).total_seconds())

            # Update session
            cursor.execute("""
                UPDATE sessions
                SET end_time = ?, duration_seconds = ?, xp_earned = ?,
                    words_learned = ?, exercises_completed = ?, mistakes_made = ?, notes = ?
                WHERE id = ?
            """, (
                end_time.isoformat(), duration_seconds, xp_earned,
                words_learned, exercises_completed, mistakes_made, notes,
                session_id
            ))

            # Update user stats
            stats = self.get_user_stats()
            new_total_time = stats['total_seconds_studied'] + duration_seconds

            self.update_user_stats(
                total_seconds_studied=new_total_time,
                last_activity_date=date.today().isoformat()
            )

            # Update daily activity
            self.update_daily_activity(duration_seconds, xp_earned, words_learned, exercises_completed)

            # Update streak
            self.update_streak(duration_seconds)

    def get_session_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get session statistics for the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) as total_sessions,
                    SUM(duration_seconds) as total_seconds,
                    SUM(xp_earned) as total_xp,
                    SUM(words_learned) as total_words,
                    SUM(exercises_completed) as total_exercises,
                    AVG(duration_seconds) as avg_duration
                FROM sessions
                WHERE start_time >= ?
            """, (cutoff_date,))

            return dict(cursor.fetchone())

    # ============================================================
    # DAILY ACTIVITY & STREAKS
    # ============================================================

    def update_daily_activity(self, duration_seconds: int, xp_earned: int,
                              words_learned: int, exercises_completed: int):
        """Update daily activity record"""
        today = date.today().isoformat()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Check if today's record exists
            cursor.execute("SELECT * FROM daily_activity WHERE date = ?", (today,))
            existing = cursor.fetchone()

            if existing:
                # Update existing record
                cursor.execute("""
                    UPDATE daily_activity
                    SET total_seconds = total_seconds + ?,
                        xp_earned = xp_earned + ?,
                        words_learned = words_learned + ?,
                        exercises_completed = exercises_completed + ?,
                        sessions_count = sessions_count + 1,
                        active = 1
                    WHERE date = ?
                """, (duration_seconds, xp_earned, words_learned, exercises_completed, today))
            else:
                # Create new record
                cursor.execute("""
                    INSERT INTO daily_activity
                    (date, total_seconds, xp_earned, words_learned, exercises_completed, sessions_count, active)
                    VALUES (?, ?, ?, ?, ?, 1, 1)
                """, (today, duration_seconds, xp_earned, words_learned, exercises_completed))

    def update_streak(self, session_duration_seconds: int):
        """Update streak based on daily activity"""
        from config import SESSION_CONFIG

        # Only count if session was long enough
        if session_duration_seconds < SESSION_CONFIG['minimum_session_seconds']:
            return

        today = date.today()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get last activity date from user stats
            stats = self.get_user_stats()
            last_activity = stats.get('last_activity_date')

            if last_activity:
                last_date = date.fromisoformat(last_activity)
                days_diff = (today - last_date).days

                if days_diff == 0:
                    # Same day, streak continues
                    pass
                elif days_diff == 1:
                    # Consecutive day, increment streak
                    new_streak = stats['streak_days'] + 1
                    longest = max(stats['longest_streak'], new_streak)
                    self.update_user_stats(streak_days=new_streak, longest_streak=longest)
                else:
                    # Streak broken, reset
                    self.update_user_stats(streak_days=1)
            else:
                # First activity
                self.update_user_stats(streak_days=1)

    def get_streak_info(self) -> Dict[str, Any]:
        """Get streak information"""
        stats = self.get_user_stats()
        return {
            'current_streak': stats['streak_days'],
            'longest_streak': stats['longest_streak'],
            'last_activity': stats.get('last_activity_date')
        }

    # ============================================================
    # ACHIEVEMENTS
    # ============================================================

    def initialize_achievements(self):
        """Initialize achievement records from config"""
        from config import ACHIEVEMENTS

        with self.get_connection() as conn:
            for achievement in ACHIEVEMENTS:
                conn.execute("""
                    INSERT OR IGNORE INTO achievements
                    (name, title, description, category, requirement_value, xp_reward, icon)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    achievement['name'],
                    achievement['title'],
                    achievement['description'],
                    achievement['category'],
                    achievement['requirement'],
                    achievement['xp'],
                    achievement['icon']
                ))

    def check_and_unlock_achievements(self) -> List[Dict]:
        """Check and unlock any earned achievements"""
        newly_unlocked = []
        stats = self.get_user_stats()
        vocab_stats = self.get_vocabulary_stats()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM achievements WHERE unlocked = 0")
            locked_achievements = cursor.fetchall()

            for achievement in locked_achievements:
                achievement = dict(achievement)
                should_unlock = False
                progress = 0

                # Check different achievement categories
                if achievement['category'] == 'streak':
                    progress = stats['streak_days']
                    should_unlock = progress >= achievement['requirement_value']

                elif achievement['category'] == 'vocabulary':
                    progress = vocab_stats['total_words']
                    should_unlock = progress >= achievement['requirement_value']

                elif achievement['category'] == 'speaking':
                    # Convert minutes to seconds for requirement
                    progress = stats['total_seconds_studied'] // 60
                    should_unlock = progress >= achievement['requirement_value']

                # Unlock if criteria met
                if should_unlock:
                    cursor.execute("""
                        UPDATE achievements
                        SET unlocked = 1, unlocked_at = ?, progress = ?
                        WHERE id = ?
                    """, (datetime.now().isoformat(), achievement['requirement_value'], achievement['id']))

                    newly_unlocked.append(achievement)
                else:
                    # Update progress
                    cursor.execute("""
                        UPDATE achievements SET progress = ? WHERE id = ?
                    """, (progress, achievement['id']))

            conn.commit()

        return newly_unlocked

    def get_achievements(self, unlocked_only: bool = False) -> List[Dict]:
        """Get all achievements"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM achievements"
            if unlocked_only:
                query += " WHERE unlocked = 1"
            query += " ORDER BY unlocked DESC, requirement_value ASC"

            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # ============================================================
    # MISTAKES TRACKING
    # ============================================================

    def log_mistake(self, session_id: int, mistake_type: str, category: str,
                   user_answer: str, correct_answer: str, explanation: str = "",
                   cefr_level: str = "", **kwargs):
        """Log a mistake for pattern analysis"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO mistakes
                (session_id, mistake_type, category, subcategory, user_answer,
                 correct_answer, explanation, grammar_rule, cefr_level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, mistake_type, category,
                kwargs.get('subcategory'),
                user_answer, correct_answer, explanation,
                kwargs.get('grammar_rule'),
                cefr_level,
                datetime.now().isoformat()
            ))

    def get_mistake_patterns(self, limit: int = 10) -> List[Dict]:
        """Get most common mistake patterns"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category, subcategory, COUNT(*) as count
                FROM mistakes
                WHERE resolved = 0
                GROUP BY category, subcategory
                ORDER BY count DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]


# Singleton instance
_db_manager = None

def get_db() -> DatabaseManager:
    """Get database manager singleton"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        _db_manager.initialize_achievements()
    return _db_manager
