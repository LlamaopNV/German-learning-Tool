-- German Learning Tool Database Schema
-- Otto von Lehrer - Your AI German Learning Buddy

-- User Statistics and Progress
CREATE TABLE IF NOT EXISTS user_stats (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Single user row
    total_xp INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 1,
    streak_days INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_date DATE,
    total_seconds_studied INTEGER DEFAULT 0,
    current_cefr_level TEXT DEFAULT 'A1', -- A1, A2, B1, B2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vocabulary Tracking with Spaced Repetition
CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    translation TEXT NOT NULL,
    cefr_level TEXT NOT NULL, -- A1, A2, B1, B2
    part_of_speech TEXT, -- noun, verb, adjective, etc.
    gender TEXT, -- der, die, das (for nouns)
    plural_form TEXT, -- for nouns
    example_sentence TEXT,
    example_translation TEXT,
    times_seen INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    times_incorrect INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP,
    next_review_date TIMESTAMP,
    ease_factor REAL DEFAULT 2.5, -- SRS ease factor
    interval_days INTEGER DEFAULT 1, -- SRS interval
    repetitions INTEGER DEFAULT 0, -- SRS repetition count
    mastered BOOLEAN DEFAULT 0,
    audio_path TEXT,
    image_path TEXT,
    source TEXT, -- PDF name or manual entry
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(word, cefr_level)
);

-- Course Progress Tracking
CREATE TABLE IF NOT EXISTS course_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL, -- e.g., "A1 Complete Course"
    cefr_level TEXT NOT NULL,
    total_sections INTEGER DEFAULT 0,
    completed_sections INTEGER DEFAULT 0,
    current_section INTEGER DEFAULT 1,
    progress_percentage REAL DEFAULT 0.0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(course_name)
);

-- Session Logs
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    xp_earned INTEGER DEFAULT 0,
    activity_type TEXT NOT NULL, -- speaking, writing, vocabulary, grammar, conversation, exam
    cefr_level TEXT, -- What level material was studied
    words_learned INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    mistakes_made INTEGER DEFAULT 0,
    notes TEXT
);

-- Exercise History
CREATE TABLE IF NOT EXISTS exercise_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    exercise_id TEXT, -- Reference to exercise in content
    exercise_type TEXT NOT NULL, -- vocabulary, grammar, reading, listening, writing, speaking
    cefr_level TEXT NOT NULL,
    topic TEXT, -- e.g., "Accusative Case", "Food Vocabulary"
    score REAL, -- Percentage or points
    max_score REAL,
    time_spent_seconds INTEGER,
    completed BOOLEAN DEFAULT 1,
    mistakes_json TEXT, -- JSON array of mistakes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Grammar Topics Progress
CREATE TABLE IF NOT EXISTS grammar_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL, -- e.g., "Nominativ", "Akkusativ", "Perfekt Tense"
    cefr_level TEXT NOT NULL,
    category TEXT, -- cases, tenses, word_order, etc.
    times_practiced INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    total_answers INTEGER DEFAULT 0,
    accuracy REAL DEFAULT 0.0,
    mastered BOOLEAN DEFAULT 0,
    last_practiced TIMESTAMP,
    notes TEXT,
    UNIQUE(topic, cefr_level)
);

-- Achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL, -- Display name
    description TEXT NOT NULL,
    category TEXT, -- streak, vocabulary, speaking, writing, exam, milestone
    requirement_value INTEGER, -- e.g., 100 for "Learn 100 words"
    xp_reward INTEGER DEFAULT 0,
    icon TEXT, -- emoji or icon identifier
    unlocked BOOLEAN DEFAULT 0,
    unlocked_at TIMESTAMP,
    progress INTEGER DEFAULT 0 -- Current progress toward achievement
);

-- Mistakes Log (for pattern analysis)
CREATE TABLE IF NOT EXISTS mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    exercise_id INTEGER,
    mistake_type TEXT NOT NULL, -- grammar, vocabulary, pronunciation, spelling
    category TEXT, -- Specific category (e.g., "article_usage", "verb_conjugation")
    subcategory TEXT, -- Even more specific (e.g., "dativ_article")
    user_answer TEXT,
    correct_answer TEXT,
    explanation TEXT,
    grammar_rule TEXT, -- Related grammar rule
    cefr_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT 0, -- If user has practiced and improved
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_history(id) ON DELETE CASCADE
);

-- Speaking Practice Log
CREATE TABLE IF NOT EXISTS speaking_practice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    scenario TEXT, -- e.g., "Ordering at a restaurant"
    cefr_level TEXT,
    duration_seconds INTEGER,
    transcription TEXT, -- Full conversation transcript
    pronunciation_score REAL, -- Average pronunciation accuracy
    fluency_score REAL,
    grammar_corrections_json TEXT, -- JSON of corrections made
    vocabulary_used_json TEXT, -- JSON of new words used
    audio_file_path TEXT, -- Local path to recording
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Writing Practice Log
CREATE TABLE IF NOT EXISTS writing_practice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    prompt TEXT NOT NULL,
    cefr_level TEXT,
    user_text TEXT NOT NULL,
    corrected_text TEXT,
    word_count INTEGER,
    grammar_errors INTEGER DEFAULT 0,
    vocabulary_score REAL, -- Richness of vocabulary
    overall_score REAL,
    feedback TEXT, -- Otto's detailed feedback
    time_spent_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Mock Exam Results
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    exam_name TEXT NOT NULL,
    cefr_level TEXT NOT NULL,
    total_score REAL NOT NULL,
    max_score REAL NOT NULL,
    percentage REAL NOT NULL,
    passed BOOLEAN DEFAULT 0,
    reading_score REAL,
    writing_score REAL,
    listening_score REAL,
    speaking_score REAL,
    time_spent_seconds INTEGER,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Daily Activity Tracking (for streak calculation and charts)
CREATE TABLE IF NOT EXISTS daily_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE NOT NULL,
    total_seconds INTEGER DEFAULT 0,
    xp_earned INTEGER DEFAULT 0,
    words_learned INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    sessions_count INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT 1 -- If minimum activity threshold met
);

-- Streaks and Milestones
CREATE TABLE IF NOT EXISTS streaks (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Single row
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    streak_freezes_available INTEGER DEFAULT 0, -- Earned through achievements
    last_freeze_used DATE
);

-- Initial Data: Create default user stats row
INSERT OR IGNORE INTO user_stats (id, current_cefr_level) VALUES (1, 'A1');

-- Initial Data: Create default streak row
INSERT OR IGNORE INTO streaks (id) VALUES (1);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vocabulary_review_date ON vocabulary(next_review_date);
CREATE INDEX IF NOT EXISTS idx_vocabulary_cefr ON vocabulary(cefr_level);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_daily_activity_date ON daily_activity(date);
CREATE INDEX IF NOT EXISTS idx_mistakes_type ON mistakes(mistake_type, category);
CREATE INDEX IF NOT EXISTS idx_exercise_history_session ON exercise_history(session_id);
