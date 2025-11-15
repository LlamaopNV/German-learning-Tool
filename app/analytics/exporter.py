"""
Statistics Exporter for GitHub Pages
Exports learning statistics to JSON for public dashboard
"""

import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sys

sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import get_db
from gamification.xp_system import get_xp_system
from gamification.srs import get_srs
from config import STATS_JSON_PATH


class StatsExporter:
    """Exports anonymized learning statistics to JSON"""

    def __init__(self):
        self.db = get_db()
        self.xp_system = get_xp_system()
        self.srs = get_srs()

    def export_stats(self) -> Dict[str, Any]:
        """
        Export all statistics to a dictionary

        Returns:
            Dict with all stats ready for JSON export
        """
        stats = {
            "last_updated": datetime.now().isoformat(),
            "overview": self._get_overview_stats(),
            "vocabulary": self._get_vocabulary_stats(),
            "skills": self._get_skills_stats(),
            "achievements": self._get_achievements_stats(),
            "daily_activity": self._get_daily_activity_stats(),
            "streak": self._get_streak_stats(),
            "exam_scores": self._get_exam_scores(),
            "milestones": self._get_milestones()
        }

        return stats

    def _get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics"""
        user_stats = self.db.get_user_stats()
        level_info = self.xp_system.get_current_level_info()

        return {
            "current_level": level_info['current_level'],
            "total_xp": level_info['current_xp'],
            "current_streak": user_stats.get('streak_days', 0),
            "longest_streak": user_stats.get('longest_streak', 0),
            "total_hours": round(user_stats['total_seconds_studied'] / 3600, 1),
            "estimated_cefr": level_info['cefr_level'],
            "started_learning": user_stats.get('created_at', datetime.now().isoformat())[:10]
        }

    def _get_vocabulary_stats(self) -> Dict[str, Any]:
        """Get vocabulary statistics"""
        vocab_stats = self.db.get_vocabulary_stats()
        srs_stats = self.srs.get_study_stats()

        return {
            "total_words": vocab_stats['total_words'],
            "by_level": vocab_stats['by_level'],
            "mastered": vocab_stats['mastered'],
            "accuracy": vocab_stats['accuracy'],
            "reviews_today": srs_stats['reviews_today']
        }

    def _get_skills_stats(self) -> Dict[str, Any]:
        """Get skill-specific statistics"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Speaking practice
            cursor.execute("""
                SELECT
                    COUNT(*) as sessions,
                    SUM(duration_seconds) as total_seconds
                FROM speaking_practice
            """)
            speaking = cursor.fetchone()

            # Writing practice
            cursor.execute("""
                SELECT
                    COUNT(*) as count,
                    AVG(overall_score) as avg_score
                FROM writing_practice
            """)
            writing = cursor.fetchone()

        return {
            "speaking_hours": round((speaking['total_seconds'] or 0) / 3600, 1),
            "speaking_sessions": speaking['sessions'] or 0,
            "writing_count": writing['count'] or 0,
            "writing_avg_score": round(writing['avg_score'] or 0, 1)
        }

    def _get_achievements_stats(self) -> List[Dict[str, Any]]:
        """Get unlocked achievements"""
        achievements = self.db.get_achievements(unlocked_only=True)

        return [
            {
                "name": ach['title'],
                "description": ach['description'],
                "icon": ach['icon'],
                "unlocked_at": ach['unlocked_at'][:10] if ach['unlocked_at'] else None,
                "category": ach['category']
            }
            for ach in achievements
        ]

    def _get_daily_activity_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get daily activity for the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).date()

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    date,
                    total_seconds,
                    xp_earned,
                    words_learned,
                    exercises_completed,
                    active
                FROM daily_activity
                WHERE date >= ?
                ORDER BY date ASC
            """, (cutoff_date.isoformat(),))

            rows = cursor.fetchall()

        return [
            {
                "date": row['date'],
                "minutes": round(row['total_seconds'] / 60, 0),
                "xp": row['xp_earned'],
                "words": row['words_learned'],
                "exercises": row['exercises_completed'],
                "active": bool(row['active'])
            }
            for row in rows
        ]

    def _get_streak_stats(self) -> Dict[str, Any]:
        """Get streak information"""
        streak_info = self.db.get_streak_info()

        return {
            "current": streak_info['current_streak'],
            "longest": streak_info['longest_streak'],
            "last_activity": streak_info.get('last_activity')
        }

    def _get_exam_scores(self) -> List[Dict[str, Any]]:
        """Get mock exam results"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    exam_name,
                    cefr_level,
                    percentage,
                    passed,
                    created_at
                FROM exam_results
                ORDER BY created_at DESC
                LIMIT 10
            """)

            rows = cursor.fetchall()

        return [
            {
                "exam": row['exam_name'],
                "level": row['cefr_level'],
                "score": round(row['percentage'], 1),
                "passed": bool(row['passed']),
                "date": row['created_at'][:10]
            }
            for row in rows
        ]

    def _get_milestones(self) -> List[Dict[str, str]]:
        """Get major milestones achieved"""
        milestones = []
        vocab_stats = self.db.get_vocabulary_stats()
        user_stats = self.db.get_user_stats()
        level_info = self.xp_system.get_current_level_info()

        # Vocabulary milestones
        total_words = vocab_stats['total_words']
        if total_words >= 2000:
            milestones.append({"milestone": "Learned 2000+ words", "icon": "🎓"})
        elif total_words >= 500:
            milestones.append({"milestone": "Learned 500+ words", "icon": "📖"})
        elif total_words >= 100:
            milestones.append({"milestone": "Learned 100+ words", "icon": "📚"})

        # Streak milestones
        longest_streak = user_stats.get('longest_streak', 0)
        if longest_streak >= 100:
            milestones.append({"milestone": "100-day streak achieved", "icon": "👑"})
        elif longest_streak >= 30:
            milestones.append({"milestone": "30-day streak achieved", "icon": "💪"})
        elif longest_streak >= 7:
            milestones.append({"milestone": "7-day streak achieved", "icon": "🔥"})

        # Study time milestones
        total_hours = user_stats['total_seconds_studied'] / 3600
        if total_hours >= 200:
            milestones.append({"milestone": "200+ hours studied", "icon": "🤖"})
        elif total_hours >= 50:
            milestones.append({"milestone": "50+ hours studied", "icon": "⏰"})
        elif total_hours >= 10:
            milestones.append({"milestone": "10+ hours studied", "icon": "📅"})

        # Level milestones
        if level_info['current_level'] >= 25:
            milestones.append({"milestone": "Reached A2 level", "icon": "🥇"})
        elif level_info['current_level'] >= 10:
            milestones.append({"milestone": "Completed A1 level", "icon": "🏅"})

        return milestones

    def save_to_file(self, stats: Dict = None) -> Path:
        """
        Save statistics to JSON file

        Args:
            stats: Stats dictionary (will export if None)

        Returns:
            Path to saved file
        """
        if stats is None:
            stats = self.export_stats()

        # Ensure directory exists
        STATS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(STATS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        return STATS_JSON_PATH

    def export_and_save(self) -> Path:
        """
        Export stats and save to file

        Returns:
            Path to saved file
        """
        stats = self.export_stats()
        return self.save_to_file(stats)


# Singleton instance
_stats_exporter = None


def get_stats_exporter() -> StatsExporter:
    """Get StatsExporter singleton"""
    global _stats_exporter
    if _stats_exporter is None:
        _stats_exporter = StatsExporter()
    return _stats_exporter


if __name__ == "__main__":
    # Command-line usage
    exporter = get_stats_exporter()
    output_path = exporter.export_and_save()
    print(f"✓ Stats exported to: {output_path}")
