"""
Configuration file for German Learning Tool
Otto von Lehrer - Your AI German Learning Buddy
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
CONTENT_DIR = BASE_DIR / "content"
COURSE_MATERIALS_DIR = BASE_DIR / "Course Materials"

# Database
DATABASE_PATH = DATA_DIR / "database.db"

# Model paths
MODELS_DIR = DATA_DIR / "models"
WHISPER_MODEL_DIR = MODELS_DIR / "whisper"
LLM_MODEL_DIR = MODELS_DIR / "llms"
VISION_MODEL_DIR = MODELS_DIR / "vision"

# Audio and recordings
AUDIO_RECORDINGS_DIR = DATA_DIR / "audio_recordings"
WRITING_SUBMISSIONS_DIR = DATA_DIR / "writing_submissions"

# Content directories
VOCABULARY_DIR = CONTENT_DIR / "vocabulary"
EXERCISES_DIR = CONTENT_DIR / "exercises"
EXAMS_DIR = CONTENT_DIR / "exams"
IMAGES_DIR = CONTENT_DIR / "images"

# GitHub Pages
GITHUB_PAGES_DIR = BASE_DIR / "docs"
STATS_JSON_PATH = GITHUB_PAGES_DIR / "data" / "stats.json"

# Create directories if they don't exist
for directory in [
    DATA_DIR, MODELS_DIR, WHISPER_MODEL_DIR, LLM_MODEL_DIR, VISION_MODEL_DIR,
    AUDIO_RECORDINGS_DIR, WRITING_SUBMISSIONS_DIR, VOCABULARY_DIR, EXERCISES_DIR,
    EXAMS_DIR, IMAGES_DIR, GITHUB_PAGES_DIR, GITHUB_PAGES_DIR / "data"
]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================
# MODEL CONFIGURATIONS
# ============================================================

# Whisper Configuration
WHISPER_CONFIG = {
    "model_size": "large-v3",  # Options: tiny, base, small, medium, large-v2, large-v3
    "device": "cuda",  # Use GPU
    "compute_type": "float16",  # float16 for GPU, int8 for CPU
    "language": "de",  # German
    "beam_size": 5,
    "vad_filter": True,  # Voice activity detection
    "vad_parameters": {
        "threshold": 0.5,
        "min_speech_duration_ms": 250,
        "max_speech_duration_s": 30,
    }
}

# LLM Configuration
LLM_CONFIG = {
    "mistral": {
        "model_name": "mistral:7b-instruct-q4_K_M",  # Ollama model
        "temperature": 0.7,
        "max_tokens": 1024,
        "use_case": "conversation, quick_responses, buddy_personality"
    },
    "llama": {
        "model_name": "llama3.1:8b-instruct-q4_K_M",  # Ollama model
        "temperature": 0.3,
        "max_tokens": 2048,
        "use_case": "corrections, detailed_explanations, essay_feedback"
    }
}

# Vision Model Configuration
VISION_CONFIG = {
    "model_name": "llava:7b-v1.6",  # Ollama vision model
    "temperature": 0.5,
    "max_tokens": 512
}

# Translation Model Configuration
TRANSLATION_CONFIG = {
    "model_name": "Helsinki-NLP/opus-mt-de-en",  # German to English
    "reverse_model": "Helsinki-NLP/opus-mt-en-de",  # English to German
    "device": "cuda"
}

# TTS Configuration
TTS_CONFIG = {
    "model": "tts_models/de/thorsten/tacotron2-DDC",  # German Thorsten voice
    "device": "cuda",
    "sample_rate": 22050
}

# ============================================================
# GAMIFICATION SETTINGS
# ============================================================

# XP System
XP_CONFIG = {
    "login_bonus": 25,
    "vocabulary_review_correct": 5,
    "vocabulary_review_incorrect": 2,
    "vocabulary_new_word": 10,
    "speaking_practice_per_minute": 5,
    "writing_exercise_short": 20,  # < 100 words
    "writing_exercise_medium": 50,  # 100-300 words
    "writing_exercise_long": 100,  # > 300 words
    "grammar_exercise_correct": 10,
    "grammar_exercise_incorrect": 5,
    "listening_exercise": 15,
    "reading_exercise": 15,
    "conversation_per_minute": 8,
    "mock_exam_completion": 200,
    "mock_exam_pass_bonus": 300,
    "streak_milestone_7_days": 50,
    "streak_milestone_30_days": 200,
    "streak_milestone_100_days": 500,
    "achievement_unlock": 100
}

# Level Progression (XP required for each level)
# Formula: XP_for_level_N = 100 * N^1.5
LEVEL_XP_REQUIREMENTS = {
    1: 0,
    2: 141,
    3: 346,
    4: 632,
    5: 968,
    6: 1342,
    7: 1747,
    8: 2179,
    9: 2635,
    10: 3114,  # End of A1
    11: 3614,
    12: 4134,
    13: 4672,
    14: 5228,
    15: 5801,
    16: 6391,
    17: 6996,
    18: 7617,
    19: 8253,
    20: 8944,
    21: 9549,
    22: 10199,
    23: 10862,
    24: 11539,
    25: 12229,  # End of A2
    26: 12933,
    27: 13649,
    28: 14378,
    29: 15120,
    30: 15875,
    # ... continues up to level 70 (B2)
}

# CEFR Level Ranges
CEFR_LEVEL_RANGES = {
    "A1": (1, 10),
    "A2": (11, 25),
    "B1": (26, 45),
    "B2": (46, 70)
}

# ============================================================
# SPACED REPETITION SETTINGS (Modified SM-2 Algorithm)
# ============================================================

SRS_CONFIG = {
    "initial_interval": 1,  # days
    "graduating_interval": 3,  # days
    "easy_interval": 7,  # days
    "minimum_ease_factor": 1.3,
    "maximum_ease_factor": 2.5,
    "starting_ease_factor": 2.5,
    "easy_bonus": 1.3,
    "hard_penalty": 0.85,
    "again_steps": [1, 10],  # minutes for re-learning
    "new_cards_per_day": 20,
    "review_cards_per_day": 100,
    "mastery_threshold": 21  # days interval before considered mastered
}

# ============================================================
# ACHIEVEMENT DEFINITIONS
# ============================================================

ACHIEVEMENTS = [
    # Streak Achievements
    {"name": "first_step", "title": "First Step", "description": "Complete your first study session",
     "category": "milestone", "requirement": 1, "xp": 50, "icon": "🎯"},
    {"name": "week_warrior", "title": "Week Warrior", "description": "Maintain a 7-day streak",
     "category": "streak", "requirement": 7, "xp": 100, "icon": "🔥"},
    {"name": "month_master", "title": "Month Master", "description": "Maintain a 30-day streak",
     "category": "streak", "requirement": 30, "xp": 300, "icon": "💪"},
    {"name": "century_scholar", "title": "Century Scholar", "description": "Maintain a 100-day streak",
     "category": "streak", "requirement": 100, "xp": 1000, "icon": "👑"},

    # Vocabulary Achievements
    {"name": "wordsmith_100", "title": "Wordsmith", "description": "Learn 100 words",
     "category": "vocabulary", "requirement": 100, "xp": 150, "icon": "📚"},
    {"name": "wordsmith_500", "title": "Word Master", "description": "Learn 500 words",
     "category": "vocabulary", "requirement": 500, "xp": 400, "icon": "📖"},
    {"name": "wordsmith_2000", "title": "Word Virtuoso", "description": "Learn 2000 words",
     "category": "vocabulary", "requirement": 2000, "xp": 1500, "icon": "🎓"},

    # Speaking Achievements
    {"name": "chatterbox_10", "title": "Chatterbox", "description": "Practice speaking for 10 hours",
     "category": "speaking", "requirement": 600, "xp": 200, "icon": "🗣️"},
    {"name": "chatterbox_50", "title": "Conversation Expert", "description": "Practice speaking for 50 hours",
     "category": "speaking", "requirement": 3000, "xp": 600, "icon": "💬"},
    {"name": "chatterbox_200", "title": "Native Talker", "description": "Practice speaking for 200 hours",
     "category": "speaking", "requirement": 12000, "xp": 2000, "icon": "🎤"},

    # Writing Achievements
    {"name": "author_50", "title": "Author", "description": "Complete 50 writing exercises",
     "category": "writing", "requirement": 50, "xp": 200, "icon": "✍️"},
    {"name": "author_200", "title": "Prolific Writer", "description": "Complete 200 writing exercises",
     "category": "writing", "requirement": 200, "xp": 600, "icon": "📝"},
    {"name": "author_500", "title": "Literary Master", "description": "Complete 500 writing exercises",
     "category": "writing", "requirement": 500, "xp": 1500, "icon": "🖊️"},

    # Exam Achievements
    {"name": "exam_a1", "title": "A1 Certified", "description": "Pass an A1 mock exam",
     "category": "exam", "requirement": 1, "xp": 300, "icon": "🏅"},
    {"name": "exam_a2", "title": "A2 Certified", "description": "Pass an A2 mock exam",
     "category": "exam", "requirement": 1, "xp": 500, "icon": "🥇"},
    {"name": "exam_b1", "title": "B1 Certified", "description": "Pass a B1 mock exam",
     "category": "exam", "requirement": 1, "xp": 800, "icon": "🏆"},
    {"name": "exam_b2", "title": "B2 Certified", "description": "Pass a B2 mock exam",
     "category": "exam", "requirement": 1, "xp": 1200, "icon": "👨‍🎓"},

    # Perfect Score Achievements
    {"name": "perfectionist_10", "title": "Perfectionist", "description": "Get 10 perfect scores",
     "category": "milestone", "requirement": 10, "xp": 150, "icon": "⭐"},
    {"name": "perfectionist_50", "title": "Flawless Master", "description": "Get 50 perfect scores",
     "category": "milestone", "requirement": 50, "xp": 500, "icon": "✨"},
    {"name": "perfectionist_100", "title": "Perfect Legend", "description": "Get 100 perfect scores",
     "category": "milestone", "requirement": 100, "xp": 1000, "icon": "💫"},

    # Study Time Achievements
    {"name": "dedicated_10", "title": "Dedicated Learner", "description": "Study for 10 hours total",
     "category": "milestone", "requirement": 600, "xp": 100, "icon": "📅"},
    {"name": "dedicated_50", "title": "Serious Student", "description": "Study for 50 hours total",
     "category": "milestone", "requirement": 3000, "xp": 400, "icon": "⏰"},
    {"name": "dedicated_200", "title": "Learning Machine", "description": "Study for 200 hours total",
     "category": "milestone", "requirement": 12000, "xp": 1500, "icon": "🤖"},
    {"name": "dedicated_500", "title": "Ultimate Scholar", "description": "Study for 500 hours total",
     "category": "milestone", "requirement": 30000, "xp": 3000, "icon": "🌟"},
]

# ============================================================
# OTTO VON LEHRER PERSONALITY SETTINGS
# ============================================================

OTTO_CONFIG = {
    "name": "Otto von Lehrer",
    "role": "Your German Learning Buddy",
    "personality_traits": [
        "encouraging", "patient", "knowledgeable", "slightly_playful",
        "celebrates_wins", "gentle_with_corrections", "adaptive"
    ],
    "greeting_messages": [
        "Guten Tag! Ready to learn some German today?",
        "Hallo! Let's make some progress together!",
        "Willkommen zurück! Your brain is ready for German!",
        "Servus! Time to level up your German skills!",
    ],
    "encouragement_messages": [
        "Ausgezeichnet! You're doing great!",
        "Wunderbar! Keep up the good work!",
        "Fantastisch! You're making real progress!",
        "Sehr gut! I'm proud of you!",
        "Großartig! You're on fire today!",
    ],
    "correction_style": "gentle",  # gentle, direct, or detailed
    "emoji_usage": True,
    "personality_prompts": {
        "base": """You are Otto von Lehrer, a friendly and encouraging German language teacher.
You are patient, knowledgeable, and slightly playful. You celebrate small wins and provide
gentle corrections. You adapt your difficulty based on the student's performance and always
maintain a positive, supportive tone. You use emojis occasionally to keep things engaging.""",

        "conversation": """You are Otto von Lehrer in a conversation practice scenario.
Stay in character, use German appropriate for the student's CEFR level, and provide
natural responses. If the student makes mistakes, gently correct them in a conversational way.""",

        "correction": """You are Otto von Lehrer providing feedback on student work.
Be thorough but encouraging. Point out mistakes clearly, explain the correct usage,
and always end with positive reinforcement about what they did well.""",
    }
}

# ============================================================
# SESSION SETTINGS
# ============================================================

SESSION_CONFIG = {
    "minimum_session_seconds": 600,  # 10 minutes for streak credit
    "auto_save_interval": 300,  # Save progress every 5 minutes
    "max_vocabulary_per_session": 20,  # Don't overwhelm user
    "difficulty_adjustment_threshold": 0.7,  # Adjust if accuracy below 70%
}

# ============================================================
# GITHUB PAGES UPDATE SETTINGS
# ============================================================

GITHUB_CONFIG = {
    "auto_push": True,  # Automatically push to GitHub after session
    "branch": "claude/work-in-progress-01Vkap9Ak5TVcqhVzo1QJcyA",
    "commit_message_template": "Update learning stats - {date}",
    "max_retries": 4,
    "retry_delays": [2, 4, 8, 16],  # Exponential backoff in seconds
}

# ============================================================
# UI SETTINGS
# ============================================================

UI_CONFIG = {
    "theme": "dark",  # dark or light
    "primary_color": "#4A90E2",  # Blue
    "secondary_color": "#50C878",  # Green
    "error_color": "#E74C3C",  # Red
    "warning_color": "#F39C12",  # Orange
    "page_icon": "🎓",
    "layout": "wide",
}
