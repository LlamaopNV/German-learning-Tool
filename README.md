# 🎓 German Learning Tool - Otto von Lehrer

Your AI-powered German learning companion! Learn German from A1 to B2 with interactive exercises, spaced repetition, gamification, and real-time progress tracking.

## 🌟 Features

### ✅ Currently Implemented (Phase 1)
- **📚 Vocabulary Builder** with Spaced Repetition System (SRS)
- **🎮 Gamification** - XP, Levels, Streaks, Achievements
- **🤖 Otto von Lehrer** - Your encouraging AI learning buddy
- **📊 Progress Tracking** - Comprehensive statistics and analytics
- **🎯 Multiple Practice Modes** - Flashcards, Multiple Choice, Fill-in-the-Blank
- **💾 Local Database** - All your data stored securely on your machine

### 🚧 Coming Soon
- **🗣️ Speech Recognition** (Whisper) - Practice speaking German
- **✍️ Writing Exercises** with AI corrections
- **👂 Listening Comprehension** - German TTS audio exercises
- **💬 Conversation Partner** - Roleplay scenarios with AI
- **🖼️ Multimodal Learning** - Image-based exercises
- **📄 PDF Import** - Process your German course materials
- **🌐 GitHub Pages Dashboard** - Public stats page

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA support (for future AI models)
- 16GB VRAM recommended (RTX 5080 or equivalent)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd German-learning-Tool
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   The database will be created automatically on first run.

5. **Run the application:**
   ```bash
   streamlit run app/main.py
   ```

6. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

---

## 📚 How to Use

### Getting Started
1. **Launch the app** using `streamlit run app/main.py`
2. **Meet Otto** - Your friendly German learning buddy will greet you
3. **Choose an activity** from the home page:
   - Review vocabulary (if you have words due)
   - Learn new words
   - Check your statistics
   - View achievements

### Vocabulary Learning Workflow

#### 1. **Learning New Words**
- Navigate to **Vocabulary → Learn New Words**
- Select your CEFR level (start with A1 if you're a beginner)
- Read through the words, examples, and translations
- Click "I've learned this word" to add it to your review queue
- Earn XP for each new word learned!

#### 2. **Reviewing Words (Spaced Repetition)**
- Go to **Vocabulary → Review Words**
- Words will appear based on SRS algorithm
- Rate how well you knew each word:
  - **Again** ❌ - Didn't remember, review soon
  - **Hard** 😐 - Difficult, shorter interval
  - **Good** ✅ - Remembered, standard interval
  - **Easy** ⭐ - Very easy, longer interval
- Earn XP for each review!

#### 3. **Track Your Progress**
- Check the **sidebar** for real-time stats
- Visit the **Statistics** page for detailed analytics
- View your **Achievements** page to see unlocked rewards

### Gamification System

- **XP (Experience Points):** Earn XP for all activities
- **Levels:** Level up from 1 to 70 (aligned with A1→B2 progress)
- **Streaks:** Maintain daily study streaks for bonus XP
- **Achievements:** Unlock 20+ achievements for milestones
- **Motivation:** Otto provides encouraging feedback throughout

---

## 🗂️ Project Structure

```
German-learning-Tool/
├── app/                          # Main application code
│   ├── main.py                   # Streamlit entry point
│   ├── config.py                 # Configuration settings
│   ├── buddy/                    # Otto's personality
│   │   └── personality.py
│   ├── database/                 # Database management
│   │   ├── schema.sql
│   │   └── db_manager.py
│   ├── gamification/             # XP, levels, SRS
│   │   ├── xp_system.py
│   │   └── srs.py
│   └── learning/                 # Learning modules
│       └── vocabulary.py
├── data/                         # Local data storage
│   ├── database.db               # SQLite database
│   ├── audio_recordings/         # Audio files (NOT synced)
│   └── models/                   # AI models
├── content/                      # Learning materials
│   ├── vocabulary/               # Word lists
│   └── exercises/                # Exercises
├── Course Materials/             # Your PDF materials
├── docs/                         # GitHub Pages (future)
└── requirements.txt
```

---

## 📊 Understanding the Spaced Repetition System (SRS)

The app uses a **Modified SM-2 algorithm** for optimal vocabulary retention:

### How it Works:
1. **New words** are reviewed after 1 day
2. **Correct answers** increase the interval (1 → 3 → 7 → 14 → 30 days...)
3. **Incorrect answers** reset to shorter intervals
4. **Mastered words** (21+ day interval) won't appear frequently

### Difficulty Ratings:
- **Again:** Reset to 1 day (for words you forgot)
- **Hard:** Shorter interval multiplier (0.85x)
- **Good:** Standard interval based on ease factor
- **Easy:** Longer interval multiplier (1.3x)

This ensures you review words right before you're about to forget them - maximizing retention!

---

## 🎮 Achievements List

Current achievements you can unlock:

### Streaks
- 🎯 **First Step** - Complete your first session
- 🔥 **Week Warrior** - 7-day streak
- 💪 **Month Master** - 30-day streak
- 👑 **Century Scholar** - 100-day streak

### Vocabulary
- 📚 **Wordsmith** - Learn 100 words
- 📖 **Word Master** - Learn 500 words
- 🎓 **Word Virtuoso** - Learn 2000 words

### Study Time
- 📅 **Dedicated Learner** - 10 hours studied
- ⏰ **Serious Student** - 50 hours studied
- 🤖 **Learning Machine** - 200 hours studied

*(More achievements coming with additional features!)*

---

## 🛠️ Advanced Configuration

### Model Configuration
Edit `app/config.py` to customize:
- **Whisper model size** (when implemented)
- **LLM selection** (Mistral vs Llama)
- **XP rewards** for different activities
- **SRS parameters** (intervals, ease factors)
- **UI settings** (theme, colors)

### Adding Vocabulary Manually

Create JSON files in `content/vocabulary/`:

```json
{
  "words": [
    {
      "word": "Hallo",
      "translation": "Hello",
      "part_of_speech": "interjection",
      "example_sentence": "Hallo, wie geht's dir?",
      "example_translation": "Hello, how are you?"
    }
  ]
}
```

Then import via the app (feature coming soon) or directly into the database.

---

## 📖 Adding Course Materials

1. **Place PDFs** in the `Course Materials/` folder
2. **PDF processing** (coming in Phase 4) will automatically extract:
   - Vocabulary words
   - Grammar exercises
   - Reading passages
   - Mock exam questions

For now, you can manually add vocabulary from your PDFs through the database or JSON import.

---

## 🎯 Learning Tips from Otto

### For Beginners (A1):
- Focus on **high-frequency words** first (the 1000 most common)
- **Review daily** - even 10 minutes helps!
- Don't stress about **grammar** initially - focus on vocabulary
- **Speak out loud** when reviewing words

### For Intermediate Learners (A2-B1):
- Start adding **context** - learn words in sentences
- Practice **writing** short paragraphs
- Focus on **common grammar patterns**
- Try **consuming German media** (shows, podcasts)

### For Advanced Learners (B2):
- Work on **less common vocabulary**
- Practice **complex sentence structures**
- Engage in **conversation** (use the conversation partner feature when available)
- Read **native German content**

---

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm data/database.db
# Restart the app - it will recreate the database
```

### Streamlit Won't Start
```bash
# Make sure you're in the virtual environment
streamlit run app/main.py --server.port 8502  # Try different port
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## 🔮 Roadmap

### Phase 2: Core Learning Features (In Progress)
- [ ] Whisper integration for speech recognition
- [ ] Writing exercises with LLM corrections
- [ ] Listening comprehension module

### Phase 3: Advanced Features
- [ ] Conversation partner with roleplay scenarios
- [ ] Vision model for image-based exercises
- [ ] PDF processing pipeline
- [ ] Mock exam system

### Phase 4: GitHub Pages Dashboard
- [ ] Real-time stats export
- [ ] Public progress dashboard
- [ ] Automated git push after sessions

---

## 🤝 Contributing

This is a personal learning tool, but suggestions are welcome! If you find bugs or have ideas for features:
1. Open an issue on GitHub
2. Describe the problem or feature request
3. Otto and I will review it!

---

## 📝 License

This project is for personal use and learning purposes.

---

## 🎓 About Otto von Lehrer

Otto von Lehrer is your friendly AI German teacher. He's:
- **Encouraging** - Celebrates your wins, big and small
- **Patient** - Gentle with corrections
- **Adaptive** - Adjusts difficulty based on your performance
- **Consistent** - Always there to support your learning journey

Otto believes that **consistency beats perfection** - so keep showing up, even for just 10 minutes a day!

---

## 📞 Support

Having issues? Check:
1. This README
2. The `/help` command in the app (coming soon)
3. GitHub issues

---

**Viel Erfolg beim Deutschlernen!** 🇩🇪

*Good luck with your German learning!*
