# 🚀 Quick Start Guide - Otto von Lehrer

Get up and running with your German learning tool in 5 minutes!

## ⚡ Fast Setup

### 1. Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Import Starter Vocabulary
```bash
# Import the 30 A1 starter words
python scripts/import_vocabulary.py
```

You should see:
```
Found 30 words at A1 level
✓ Added: Hallo
✓ Added: danke
...
Import complete!
Added: 30 words
```

### 3. Launch the App
```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📚 First Steps in the App

### Meet Otto von Lehrer!
Otto will greet you on the home page. He's your friendly AI learning buddy who will:
- Celebrate your progress
- Provide gentle corrections
- Keep you motivated with encouragement

### Start Learning Vocabulary

#### Option 1: Review Mode (Spaced Repetition)
1. Click **"Vocabulary"** in the sidebar
2. Go to **"Review Words"** tab
3. Click **"Start Review Session"**
4. For each word:
   - Try to recall the translation
   - Click **"Show Answer"**
   - Rate yourself: **Again**, **Hard**, **Good**, or **Easy**
5. Earn XP and watch your progress grow!

#### Option 2: Learn New Words
1. Click **"Vocabulary"** → **"Learn New Words"**
2. Select **A1** level (you're starting fresh!)
3. Read through the words, translations, and examples
4. Click **"I've learned this word"** for each one
5. Words are added to your review queue automatically

---

## 🎮 Understanding the Gamification

### XP (Experience Points)
- **Vocabulary review (correct):** +5 XP
- **Vocabulary review (incorrect):** +2 XP (you still tried!)
- **New word learned:** +10 XP
- **Daily login bonus:** +25 XP

### Levels
- Level 1-10: A1 (Beginner)
- Level 11-25: A2 (Elementary)
- Level 26-45: B1 (Intermediate)
- Level 46-70: B2 (Upper Intermediate)

### Achievements
Unlock achievements by:
- Maintaining streaks (7, 30, 100 days)
- Learning words (100, 500, 2000)
- Studying hours (10, 50, 200)
- Getting perfect scores

### Streaks
- Study at least 10 minutes per day to maintain your streak
- Check the sidebar to see your current streak 🔥
- Otto gets extra excited about long streaks!

---

## 🧠 How Spaced Repetition Works

The app uses an SRS (Spaced Repetition System) to optimize your learning:

1. **New words** appear after 1 day
2. **Correct answers** increase the interval (3 days → 7 days → 14 days → 30 days...)
3. **Incorrect answers** reset to shorter intervals
4. **Mastered words** (21+ day interval) appear less frequently

### Rating Guide:
- **Again (❌):** You forgot it → Review in 1 day
- **Hard (😐):** Difficult to remember → Review in 2-3 days
- **Good (✅):** You remembered → Standard interval
- **Easy (⭐):** Very easy → Longer interval (skip ahead)

**Tip:** Be honest with yourself! The system works best when you accurately rate your recall.

---

## 📖 Adding Your Own Vocabulary

### Option 1: Place PDFs in Course Materials
1. Put your German course PDFs in the `Course Materials/` folder
2. PDF processing feature coming in Phase 4!

### Option 2: Create JSON Files
Create a file in `content/vocabulary/my_words.json`:

```json
{
  "name": "My Custom Vocabulary",
  "cefr_level": "A1",
  "words": [
    {
      "word": "der Apfel",
      "translation": "the apple",
      "part_of_speech": "noun",
      "gender": "der",
      "plural_form": "die Äpfel",
      "example_sentence": "Der Apfel ist rot.",
      "example_translation": "The apple is red."
    }
  ]
}
```

Then import:
```bash
python scripts/import_vocabulary.py
```

---

## 🎯 Daily Routine Suggestions

### Beginner (10-15 minutes/day):
1. Review due words (5 min)
2. Learn 5 new words (5 min)
3. Re-review any difficult words (5 min)

### Intermediate (20-30 minutes/day):
1. Review due words (10 min)
2. Learn 10 new words (10 min)
3. Grammar/writing practice (10 min) ← Coming soon!

### Advanced (30-60 minutes/day):
1. Review words (10 min)
2. Conversation practice (20 min) ← Coming soon!
3. Writing exercises (20 min) ← Coming soon!
4. Mock exams (10 min) ← Coming soon!

---

## 💡 Tips from Otto

### For Maximum Retention:
1. **Consistency > Intensity:** Better to study 15 minutes daily than 2 hours once a week
2. **Review before bed:** Your brain consolidates memory during sleep
3. **Speak out loud:** Even when reviewing silently, say the words out loud
4. **Use context:** Pay attention to example sentences, not just translations
5. **Trust the SRS:** Review what the system shows you, in the order shown

### Dealing with Difficult Words:
- If a word keeps appearing, that's good! It means you need more practice
- Try creating your own memorable sentence with the word
- Look up the word online for more context and usage examples
- Associate the word with an image or personal memory

### Building Streaks:
- Set a specific time each day for learning (morning coffee, before bed, etc.)
- Enable notifications (coming soon!)
- Use streak freeze rewards for days you absolutely can't study
- Remember: Even 10 minutes counts!

---

## 🐛 Troubleshooting

### "No words available for review"
- Make sure you've imported vocabulary: `python scripts/import_vocabulary.py`
- Learn some new words first, then they'll appear for review tomorrow

### "Database error"
```bash
# Delete and recreate the database
rm data/database.db
streamlit run app/main.py
# Re-import vocabulary
python scripts/import_vocabulary.py
```

### "Port already in use"
```bash
# Use a different port
streamlit run app/main.py --server.port 8502
```

---

## 🚀 What's Next?

### Coming in Future Updates:
- 🗣️ **Speaking Practice** with Whisper (talk to Otto!)
- ✍️ **Writing Exercises** with AI corrections
- 👂 **Listening Comprehension** with German TTS
- 💬 **Conversation Partner** for roleplay scenarios
- 🖼️ **Image-based Exercises** from your PDFs
- 📊 **GitHub Pages Dashboard** to show off your progress

### Want to Contribute Ideas?
Open an issue on GitHub with your suggestions!

---

## 📞 Need Help?

- Check the main **README.md** for detailed documentation
- Review your statistics page in the app
- Watch Otto's tips and encouragement in the sidebar

---

**Viel Erfolg!** (Good luck!)

Now go forth and learn German with Otto! 🇩🇪🎓

*Remember: Every word learned is a step closer to fluency!*
