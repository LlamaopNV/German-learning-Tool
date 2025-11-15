# 🌐 GitHub Pages Setup Guide

Quick guide to enable your German Learning Tool dashboard!

## ✅ What You Already Have

All the dashboard files are ready:
- ✅ `docs/index.html` - Dashboard HTML
- ✅ `docs/css/style.css` - Dark theme styling
- ✅ `docs/js/stats.js` - Chart.js visualizations
- ✅ `docs/data/stats.json` - Your learning statistics
- ✅ `scripts/export_and_push_stats.py` - Auto-export script

## 🚀 Quick Setup (3 Steps)

### Step 1: Enable GitHub Pages on Your Repository

1. Go to your repository on GitHub: `https://github.com/LlamaopNV/German-learning-Tool`
2. Click **Settings** (top right)
3. Click **Pages** in the left sidebar
4. Under **"Build and deployment"**:
   - **Source:** Deploy from a branch
   - **Branch:** Select `claude/work-in-progress-01Vkap9Ak5TVcqhVzo1QJcyA` (or your main branch)
   - **Folder:** Select `/docs`
   - Click **Save**

### Step 2: Wait for Deployment (1-2 minutes)

GitHub will automatically build and deploy your site. You'll see:
- ✅ A green checkmark when ready
- 🌐 Your dashboard URL: `https://llamaopnv.github.io/German-learning-Tool/`

### Step 3: Test Your Dashboard

Visit your dashboard URL and you should see:
- Overview cards (Level, XP, Streak, Hours)
- CEFR progress bars
- Daily activity chart
- Achievements grid
- Milestones

## 📊 Updating Your Stats

### Manual Update:
```bash
python scripts/export_and_push_stats.py
```

This will:
1. Export your latest stats to `docs/data/stats.json`
2. Commit the changes
3. Push to GitHub (with retry logic)
4. Your dashboard updates automatically!

### Automatic Updates (Coming Soon):
The app will auto-export stats after each study session!

## 🎨 Dashboard Features

Your dashboard shows:
- ✅ **Current Level & XP** - Your gamification progress
- ✅ **Study Streak** - Current and longest streaks
- ✅ **Total Hours** - Time invested in learning
- ✅ **Vocabulary Stats** - Words learned, mastery rate, accuracy
- ✅ **CEFR Progress** - Visual progress through A1 → A2 → B1 → B2
- ✅ **Daily Activity Chart** - Last 30 days (minutes & XP)
- ✅ **Achievements** - All unlocked achievements with icons
- ✅ **Milestones** - Major accomplishments

## 🔧 Customization

### Change Auto-Push Settings:

Edit `app/config.py`:
```python
GITHUB_CONFIG = {
    "auto_push": True,  # Enable/disable
    "branch": "your-branch-name",
    "max_retries": 4,
    "retry_delays": [2, 4, 8, 16]
}
```

### Dashboard Colors:

The dashboard uses the same color scheme as your Streamlit app:
- **Primary:** `#4A90E2` (Blue)
- **Background:** `#0E1117` (Dark)
- **Cards:** `#262730` (Dark gray)

To customize, edit `docs/css/style.css`.

## 🐛 Troubleshooting

### Dashboard Not Loading?
1. Wait 2-3 minutes after enabling GitHub Pages
2. Check that `/docs` folder is selected in Settings → Pages
3. Verify the branch has the docs/ folder with all files

### Stats Not Updating?
1. Run `python scripts/export_and_push_stats.py` manually
2. Check that `docs/data/stats.json` exists
3. Verify the file was committed and pushed to GitHub

### 404 Error?
1. Make sure GitHub Pages is enabled
2. Check the branch and folder settings
3. Verify the URL: `https://YOUR-USERNAME.github.io/REPO-NAME/`

## 📈 What Gets Tracked

✅ **Public Stats:**
- Level, XP, streak, hours
- Vocabulary counts (no specific words)
- Achievements unlocked
- Daily activity (last 30 days)
- Exam scores

❌ **NOT Tracked (Privacy):**
- Specific vocabulary words
- Audio recordings
- Personal information
- Writing submissions

## 🎯 Next Steps

1. ✅ Enable GitHub Pages (see Step 1)
2. ✅ Study some German in the app
3. ✅ Run `python scripts/export_and_push_stats.py`
4. ✅ Share your progress with friends!

---

**Questions?** Check the main [README.md](README.md) for more details!

**Viel Erfolg!** 🇩🇪
