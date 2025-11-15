# 🎓 German Learning Tool - Otto von Lehrer

Your AI-powered German learning companion! Learn German from A1 to B2 with interactive exercises, spaced repetition, gamification, and real-time progress tracking.

## 🌟 Features

### ✅ Currently Implemented
- **📚 Vocabulary System** - 98 A1 words with Spaced Repetition (SRS)
- **🎯 Quiz Mode** - Multiple-choice testing with 4 answer options
- **💬 Conversation Partner** - 7 AI roleplay scenarios (A1-B2)
- **🤖 Otto von Lehrer** - Your encouraging AI learning buddy
- **🎮 Gamification** - XP, Levels (1-70), Streaks, 20+ Achievements
- **📊 Progress Tracking** - Comprehensive statistics and analytics
- **🎭 Roleplay Scenarios** - Café, shopping, directions, doctor, job interview, debates
- **🧠 LLM Integration** - Ollama support (Mistral/Llama) with mock fallback
- **💾 Local Database** - All your data stored securely on your machine
- **🌐 GitHub Pages Dashboard** - Public stats page with real-time updates

### 🚧 Coming Soon
- **🗣️ Speech Recognition** (Whisper) - Speak instead of type
- **✍️ Writing Exercises** with AI corrections
- **👂 Listening Comprehension** - German TTS audio exercises
- **🖼️ Multimodal Learning** - Image-based exercises
- **📄 PDF Import** - Automatic extraction from your materials

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- **Optional:** Ollama (for AI-powered conversations - see below)
- **Optional:** NVIDIA GPU with CUDA support (for future speech features)
- **Optional:** 16GB VRAM recommended (RTX 5080 or equivalent)

### Optional: Install Ollama for AI Conversations

The Conversation Partner feature works with **mock responses** out of the box, but for real AI-powered conversations, install Ollama:

**Windows:**
1. Download Ollama from https://ollama.ai
2. Run the installer
3. Open PowerShell and pull a model:
   ```powershell
   ollama pull mistral:7b-instruct-q4_K_M
   ```
4. The app will automatically detect and use Ollama!

**Note:** Mistral 7B (4-bit) uses ~4GB of VRAM. Llama 3.1 8B uses ~5GB.

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

4. **Import vocabulary:**
   ```bash
   python scripts/import_vocabulary.py
   ```
   This loads **98 A1 German words** to get you started!

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

#### 3. **Quiz Mode (Multiple Choice)**
- Go to **Vocabulary → Quiz Mode**
- Select your level and click **"Start Quiz"**
- Answer multiple-choice questions (4 options per question)
- Get instant feedback on correct/incorrect answers
- **Correct answers** → Word marked as "good" in SRS (appears less)
- **Wrong answers** → Word marked as "again" in SRS (more practice)
- See your final score and earn XP!

#### 4. **Track Your Progress**
- Check the **sidebar** for real-time stats
- Visit the **Statistics** page for detailed analytics
- View your **Achievements** page to see unlocked rewards

### Conversation Partner

Practice real German conversations with Otto through roleplay scenarios!

#### How to Use:
1. Click **💬 Conversation** in the sidebar
2. Select your CEFR level (A1-B2)
3. Choose a scenario:
   - **A1:** Greeting & Introduction, Ordering at Café, Shopping
   - **A2:** Asking for Directions, At the Doctor
   - **B1:** Job Interview
   - **B2:** Discussing Current Events
4. Chat with Otto in German (type your responses)
5. Otto responds in-character based on the scenario
6. End conversation to see your stats and earn XP!

**With Ollama:** Get real AI-powered, context-aware responses
**Without Ollama:** Use pre-programmed mock responses for practice

### Gamification System

- **XP (Experience Points):** Earn XP for all activities
- **Levels:** Level up from 1 to 70 (aligned with A1→B2 progress)
- **Streaks:** Maintain daily study streaks for bonus XP
- **Achievements:** Unlock 20+ achievements for milestones
- **Motivation:** Otto provides encouraging feedback throughout

---

## 🌐 GitHub Pages Dashboard

Track your German learning progress publicly with the automated stats dashboard!

### 📊 What's Included:

The dashboard displays:
- **Overview Cards:** Current level, total XP, streak, and hours studied
- **CEFR Progress Bars:** Visual progress through A1 → A2 → B1 → B2
- **Vocabulary Stats:** Words learned by level, mastery rate, accuracy
- **Daily Activity Chart:** Last 30 days of study time and XP (Chart.js)
- **Achievements Grid:** All unlocked achievements with icons
- **Milestones:** Major accomplishments (100 words, 7-day streak, etc.)

### 🚀 Setup Instructions:

#### 1. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source", select **Deploy from a branch**
   - Branch: Select your main branch (or the branch with the `docs/` folder)
   - Folder: Select **`/docs`**
   - Click **Save**

#### 2. **Configure Auto-Push (Optional)**

   Edit `app/config.py` to customize the auto-push settings:
   ```python
   GITHUB_CONFIG = {
       'auto_push': True,  # Enable/disable auto-push
       'branch': 'your-branch-name',  # Branch to push to
       'max_retries': 4,
       'retry_delays': [2, 4, 8, 16]  # Exponential backoff
   }
   ```

#### 3. **Export and Push Stats**

   **Manual Export:**
   ```bash
   python scripts/export_and_push_stats.py
   ```

   This will:
   - ✅ Export your stats to `docs/data/stats.json`
   - ✅ Commit the changes
   - ✅ Push to GitHub (with retry logic)
   - ✅ Display your dashboard URL

   **Automatic Export (Coming Soon):**
   The app will automatically export stats after each session!

#### 4. **View Your Dashboard**

   After GitHub Pages builds (1-2 minutes), visit:
   ```
   https://YOUR-USERNAME.github.io/German-learning-Tool/
   ```

### 🎨 Dashboard Features:

- **Dark Theme:** Matches the Streamlit app's color scheme
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Chart.js Visualizations:** Interactive charts for activity tracking
- **Real-time Updates:** Stats refresh whenever you push new data
- **Anonymized Data:** No personal information, just learning progress
- **Zero Configuration:** Works out of the box!

### 📈 What Gets Tracked:

✅ **Overview:** Level, XP, streak, hours, CEFR estimate
✅ **Vocabulary:** Total words, by level, mastered, accuracy
✅ **Skills:** Speaking hours/sessions, writing count/scores
✅ **Daily Activity:** Last 30 days (minutes, XP, words, exercises)
✅ **Achievements:** All unlocked achievements with dates
✅ **Exam Results:** Mock exam scores and pass/fail status
✅ **Milestones:** Major accomplishments

❌ **NOT Tracked:** Personal info, specific word lists, audio recordings

---

## 🗂️ Project Structure

```
German-learning-Tool/
├── app/                          # Main application code
│   ├── main.py                   # Streamlit entry point
│   ├── config.py                 # Configuration settings
│   ├── analytics/                # Stats export system
│   │   └── exporter.py
│   ├── buddy/                    # Otto's personality
│   │   ├── personality.py
│   │   └── conversation.py
│   ├── database/                 # Database management
│   │   ├── schema.sql
│   │   └── db_manager.py
│   ├── gamification/             # XP, levels, SRS
│   │   ├── xp_system.py
│   │   └── srs.py
│   ├── learning/                 # Learning modules
│   │   └── vocabulary.py
│   └── models/                   # LLM integration
│       └── llm_manager.py
├── data/                         # Local data storage
│   ├── database.db               # SQLite database
│   ├── audio_recordings/         # Audio files (NOT synced)
│   └── models/                   # AI models
├── content/                      # Learning materials
│   ├── vocabulary/               # Word lists (98 A1 words)
│   └── exercises/                # Exercises
├── docs/                         # GitHub Pages dashboard
│   ├── index.html                # Dashboard HTML
│   ├── css/style.css             # Dark theme styling
│   ├── js/stats.js               # Chart.js visualizations
│   └── data/stats.json           # Exported statistics
├── scripts/                      # Utility scripts
│   ├── import_vocabulary.py
│   └── export_and_push_stats.py
├── Course Materials/             # Your PDF materials
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

### ✅ Phase 1: Foundation (Complete)
- [x] Vocabulary system with SRS
- [x] Quiz mode with multiple choice
- [x] Gamification (XP, levels, achievements)
- [x] Conversation partner with roleplay scenarios
- [x] LLM integration (Ollama)
- [x] GitHub Pages dashboard with real-time stats

### Phase 2: Core Learning Features (In Progress)
- [ ] Whisper integration for speech recognition
- [ ] Writing exercises with LLM corrections
- [ ] Listening comprehension module

### Phase 3: Advanced Features
- [ ] Vision model for image-based exercises
- [ ] PDF processing pipeline
- [ ] Mock exam system with A1-B2 tests

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
