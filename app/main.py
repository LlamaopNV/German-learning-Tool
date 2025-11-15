"""
German Learning Tool - Main Application
Otto von Lehrer - Your AI German Learning Buddy

Run with: streamlit run app/main.py
"""

import streamlit as st
from pathlib import Path
import sys

# Add app directory to path
sys.path.append(str(Path(__file__).parent))

from database.db_manager import get_db
from gamification.xp_system import get_xp_system
from gamification.srs import get_srs
from buddy.personality import get_otto
from learning.vocabulary import get_vocabulary_learner
from buddy.conversation import get_conversation_manager
from models.llm_manager import get_llm
from config import UI_CONFIG

# Page configuration
st.set_page_config(
    page_title="Otto von Lehrer - German Learning Tool",
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# Initialize systems
db = get_db()
xp_system = get_xp_system()
srs = get_srs()
otto = get_otto()
vocab_learner = get_vocabulary_learner()
conversation_manager = get_conversation_manager()
llm = get_llm()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'review_mode' not in st.session_state:
    st.session_state.review_mode = None


def render_sidebar():
    """Render the sidebar with Otto and user stats"""
    with st.sidebar:
        # Otto avatar and greeting
        st.markdown("### 🎓 Otto von Lehrer")
        st.caption("Your German Learning Buddy")

        st.divider()

        # User stats
        stats = db.get_user_stats()
        level_info = xp_system.get_current_level_info()
        streak_info = db.get_streak_info()

        # Level and XP
        st.markdown(f"**Level {level_info['current_level']}** ({level_info['cefr_level']})")

        # XP Progress bar
        st.progress(
            level_info['progress_percentage'] / 100,
            text=f"{level_info['xp_progress']}/{level_info['xp_needed_for_next']} XP"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total XP", f"{level_info['current_xp']:,}")
        with col2:
            st.metric("🔥 Streak", f"{streak_info['current_streak']} days")

        st.divider()

        # Today's progress
        st.markdown("#### Today's Progress")
        # TODO: Get today's stats from daily_activity table
        st.metric("⏱️ Minutes", "0")
        st.metric("📚 Words Learned", "0")
        st.metric("⭐ XP Earned", "0")

        st.divider()

        # Navigation
        st.markdown("#### Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

        if st.button("📚 Vocabulary", use_container_width=True):
            st.session_state.page = 'vocabulary'
            st.rerun()

        if st.button("💬 Conversation", use_container_width=True):
            st.session_state.page = 'conversation'
            st.rerun()

        if st.button("📊 Statistics", use_container_width=True):
            st.session_state.page = 'stats'
            st.rerun()

        if st.button("🏆 Achievements", use_container_width=True):
            st.session_state.page = 'achievements'
            st.rerun()

        st.divider()

        # Otto's daily tip
        with st.expander("💡 Otto's Daily Tip"):
            st.info(otto.get_daily_reminder())


def render_home_page():
    """Render the home page"""
    st.title("🎓 Welcome to Otto von Lehrer!")

    # Otto's greeting
    st.markdown(f"## {otto.get_greeting()}")

    # Quick stats overview
    stats = db.get_user_stats()
    srs_stats = srs.get_study_stats()
    vocab_stats = vocab_learner.get_vocabulary_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Vocabulary",
            f"{vocab_stats['total_words']} words",
            delta=f"{vocab_stats['mastered']} mastered"
        )

    with col2:
        st.metric(
            "📝 Due Reviews",
            srs_stats['due_reviews'],
            help="Words ready for review"
        )

    with col3:
        hours_studied = stats['total_seconds_studied'] / 3600
        st.metric(
            "⏱️ Study Time",
            f"{hours_studied:.1f} hrs",
            help="Total time spent studying"
        )

    with col4:
        st.metric(
            "🎯 Accuracy",
            f"{vocab_stats['accuracy']:.0f}%",
            help="Overall vocabulary accuracy"
        )

    st.divider()

    # Recommendations
    st.markdown("### 🎯 What would you like to do today?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📚 Vocabulary Practice")
        if srs_stats['due_reviews'] > 0:
            st.info(f"✨ {srs_stats['due_reviews']} words ready for review!")
            if st.button("Start Review Session", use_container_width=True, type="primary"):
                st.session_state.page = 'vocabulary'
                st.session_state.review_mode = 'review'
                st.rerun()
        else:
            st.success("🎉 No reviews due! You're all caught up!")

        if srs_stats['new_words_available'] > 0:
            st.info(f"🌟 {srs_stats['new_words_available']} new words available!")
            if st.button("Learn New Words", use_container_width=True):
                st.session_state.page = 'vocabulary'
                st.session_state.review_mode = 'learn'
                st.rerun()

    with col2:
        st.markdown("#### 📈 Your Progress")

        # Show recent achievements
        achievements = db.get_achievements(unlocked_only=True)
        recent_achievements = achievements[:3] if achievements else []

        if recent_achievements:
            st.success(f"🏆 {len(achievements)} achievements unlocked!")
            for ach in recent_achievements:
                st.markdown(f"{ach['icon']} **{ach['title']}**")
        else:
            st.info("🎯 Complete activities to unlock achievements!")

        if st.button("View All Achievements", use_container_width=True):
            st.session_state.page = 'achievements'
            st.rerun()

    st.divider()

    # Otto's motivational quote
    st.markdown("### 💭 Otto says:")
    st.markdown(f"> {otto.get_random_otto_quote()}")


def render_vocabulary_page():
    """Render the vocabulary practice page"""
    st.title("📚 Vocabulary Practice")

    # Tab selection
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Review Words", "🌟 Learn New", "🎯 Quiz Mode", "📊 Statistics"])

    with tab1:
        render_vocabulary_review()

    with tab2:
        render_vocabulary_learn()

    with tab3:
        render_vocabulary_quiz()

    with tab4:
        render_vocabulary_stats()


def render_vocabulary_review():
    """Render vocabulary review interface"""
    st.markdown("### 📝 Review Session")

    # Get due reviews
    review_words = vocab_learner.get_review_session(limit=20)

    if not review_words:
        st.success("🎉 No words due for review! Great job staying on top of things!")
        st.info("💡 Check back tomorrow, or learn some new words!")
        return

    st.info(f"📚 {len(review_words)} words ready for review")

    # Start session if not started
    if 'vocab_session_started' not in st.session_state:
        if st.button("Start Review Session", type="primary"):
            session_info = vocab_learner.start_session(cefr_level='A1')
            st.session_state.vocab_session_started = True
            st.session_state.current_word_index = 0
            st.session_state.review_words = review_words
            st.rerun()
        return

    # Review session active
    if st.session_state.current_word_index >= len(st.session_state.review_words):
        # Session complete
        st.success("🎉 Review session complete!")
        summary = vocab_learner.end_session()

        st.markdown(summary['otto_summary'])

        # Show stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Reviews", summary['session_stats']['reviews_completed'])
        with col2:
            st.metric("Accuracy", f"{summary['accuracy']:.0f}%")
        with col3:
            st.metric("XP Earned", summary['session_stats']['xp_earned'])

        # New achievements
        if summary['new_achievements']:
            st.balloons()
            for ach in summary['new_achievements']:
                st.markdown(otto.celebrate_achievement(ach))

        if st.button("Start Another Session"):
            del st.session_state.vocab_session_started
            del st.session_state.current_word_index
            del st.session_state.review_words
            st.rerun()

        return

    # Current word
    current_word = st.session_state.review_words[st.session_state.current_word_index]

    # Progress
    progress = (st.session_state.current_word_index + 1) / len(st.session_state.review_words)
    st.progress(progress, text=f"Word {st.session_state.current_word_index + 1} of {len(st.session_state.review_words)}")

    # Flashcard
    st.markdown("---")
    st.markdown(f"## {current_word['word']}")

    if current_word.get('gender'):
        st.caption(f"*{current_word['gender']} ({current_word.get('part_of_speech', '')})*")

    # Show answer
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False

    if not st.session_state.show_answer:
        if st.button("Show Answer", type="primary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    else:
        # Show translation
        st.markdown(f"### Translation: {current_word['translation']}")

        if current_word.get('example_sentence'):
            with st.expander("📖 Example"):
                st.markdown(f"**{current_word['example_sentence']}**")
                if current_word.get('example_translation'):
                    st.caption(current_word['example_translation'])

        st.markdown("### How well did you know this word?")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("❌ Again", use_container_width=True):
                result = vocab_learner.review_word(current_word['id'], "", 'again')
                st.session_state.last_result = result
                st.session_state.current_word_index += 1
                st.session_state.show_answer = False
                st.rerun()

        with col2:
            if st.button("😐 Hard", use_container_width=True):
                result = vocab_learner.review_word(current_word['id'], "", 'hard')
                st.session_state.last_result = result
                st.session_state.current_word_index += 1
                st.session_state.show_answer = False
                st.rerun()

        with col3:
            if st.button("✅ Good", use_container_width=True):
                result = vocab_learner.review_word(current_word['id'], "", 'good')
                st.session_state.last_result = result
                st.session_state.current_word_index += 1
                st.session_state.show_answer = False
                st.rerun()

        with col4:
            if st.button("⭐ Easy", use_container_width=True):
                result = vocab_learner.review_word(current_word['id'], "", 'easy')
                st.session_state.last_result = result
                st.session_state.current_word_index += 1
                st.session_state.show_answer = False
                st.rerun()

    # Show last result feedback
    if 'last_result' in st.session_state and st.session_state.show_answer == False:
        result = st.session_state.last_result
        st.success(f"{result['feedback']} +{result['xp_gained']} XP")
        if result['leveled_up']:
            st.balloons()
            st.success("🎉 LEVEL UP!")


def render_vocabulary_learn():
    """Render learn new words interface"""
    st.markdown("### 🌟 Learn New Words")

    # Select CEFR level
    cefr_level = st.selectbox(
        "Choose your level:",
        ["A1", "A2", "B1", "B2"],
        index=0,
        help="Start with A1 if you're a beginner"
    )

    # Get new words
    new_words = vocab_learner.get_new_words(cefr_level, limit=10)

    if not new_words:
        st.warning(f"No new words available for {cefr_level} level.")
        st.info("💡 Add vocabulary from PDFs or wait for more content to be added!")
        return

    st.success(f"🌟 {len(new_words)} new words available in {cefr_level}")

    # Display words in a nice format
    for i, word in enumerate(new_words[:5], 1):  # Show first 5
        with st.expander(f"{i}. {word['word']} - {word['translation']}", expanded=(i == 1)):
            if word.get('gender'):
                st.markdown(f"**Gender:** {word['gender']}")
            if word.get('part_of_speech'):
                st.markdown(f"**Type:** {word['part_of_speech']}")
            if word.get('plural_form'):
                st.markdown(f"**Plural:** {word['plural_form']}")
            if word.get('example_sentence'):
                st.markdown("**Example:**")
                st.markdown(f"*{word['example_sentence']}*")
                if word.get('example_translation'):
                    st.caption(word['example_translation'])

            if st.button(f"✅ I've learned this word", key=f"learn_{word['id']}"):
                result = vocab_learner.learn_new_word(word['id'])
                st.success(f"{result['feedback']} +{result['xp_gained']} XP")
                st.rerun()


def render_vocabulary_quiz():
    """Render multiple-choice quiz mode"""
    st.markdown("### 🎯 Multiple Choice Quiz")
    st.info("Test your knowledge! Select the correct English translation for each German word.")

    # Get learned words (words that have been seen at least once)
    with vocab_learner.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM vocabulary
            WHERE times_seen > 0
            ORDER BY RANDOM()
            LIMIT 20
        """)
        learned_words = [dict(row) for row in cursor.fetchall()]

    if not learned_words:
        st.warning("📚 No words learned yet! Go to 'Learn New Words' tab first.")
        return

    st.success(f"🎓 Quiz ready with {len(learned_words)} words!")

    # Start quiz session
    if 'quiz_session_started' not in st.session_state:
        if st.button("Start Quiz", type="primary", use_container_width=True):
            session_info = vocab_learner.start_session(cefr_level='A1')
            st.session_state.quiz_session_started = True
            st.session_state.quiz_current_index = 0
            st.session_state.quiz_words = learned_words
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = []
            st.rerun()
        return

    # Quiz in progress
    if st.session_state.quiz_current_index >= len(st.session_state.quiz_words):
        # Quiz complete!
        st.success("🎉 Quiz Complete!")

        total_questions = len(st.session_state.quiz_words)
        correct_answers = st.session_state.quiz_score
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions", total_questions)
        with col2:
            st.metric("Correct", correct_answers)
        with col3:
            st.metric("Accuracy", f"{accuracy:.0f}%")

        # End session
        summary = vocab_learner.end_session()
        st.markdown(summary['otto_summary'])

        # New achievements
        if summary.get('new_achievements'):
            st.balloons()
            for ach in summary['new_achievements']:
                st.markdown(otto.celebrate_achievement(ach))

        if st.button("Start New Quiz"):
            del st.session_state.quiz_session_started
            del st.session_state.quiz_current_index
            del st.session_state.quiz_words
            del st.session_state.quiz_score
            del st.session_state.quiz_answers
            st.rerun()

        return

    # Current question
    current_word = st.session_state.quiz_words[st.session_state.quiz_current_index]

    # Progress
    progress = (st.session_state.quiz_current_index + 1) / len(st.session_state.quiz_words)
    st.progress(progress, text=f"Question {st.session_state.quiz_current_index + 1} of {len(st.session_state.quiz_words)}")

    # Generate multiple choice question
    quiz_question = vocab_learner.multiple_choice_mode(current_word, num_choices=4)

    st.markdown("---")
    st.markdown(f"## What does **{quiz_question['word']}** mean?")

    if current_word.get('gender'):
        st.caption(f"*{current_word['gender']} ({current_word.get('part_of_speech', '')})*")

    # Show hint if available
    if 'show_hint' not in st.session_state:
        st.session_state.show_hint = False

    if quiz_question['hint'] and not st.session_state.show_hint:
        if st.button("💡 Show Hint"):
            st.session_state.show_hint = True
            st.rerun()

    if st.session_state.show_hint and quiz_question['hint']:
        st.info(f"📖 Example: {quiz_question['hint']}")

    # Answer buttons
    st.markdown("### Choose the correct translation:")

    if 'answer_selected' not in st.session_state:
        st.session_state.answer_selected = False
        st.session_state.selected_answer = None

    if not st.session_state.answer_selected:
        # Show answer choices as buttons
        for i, choice in enumerate(quiz_question['choices']):
            if st.button(choice, key=f"choice_{i}", use_container_width=True):
                st.session_state.answer_selected = True
                st.session_state.selected_answer = choice
                st.rerun()
    else:
        # Show result
        is_correct = st.session_state.selected_answer == quiz_question['correct_answer']

        if is_correct:
            st.success(f"✅ Correct! {otto.get_encouragement('correct')}")
            st.session_state.quiz_score += 1
            # Update vocab as 'good' in SRS
            result = vocab_learner.review_word(current_word['id'], "", 'good')
        else:
            st.error(f"❌ Not quite! The correct answer was: **{quiz_question['correct_answer']}**")
            st.info(otto.get_encouragement('incorrect'))
            # Update vocab as 'again' in SRS
            result = vocab_learner.review_word(current_word['id'], "", 'again')

        st.caption(f"+{result['xp_gained']} XP")

        # Next button
        if st.button("Next Question ➡️", type="primary", use_container_width=True):
            st.session_state.quiz_current_index += 1
            st.session_state.answer_selected = False
            st.session_state.selected_answer = None
            st.session_state.show_hint = False
            st.rerun()


def render_vocabulary_stats():
    """Render vocabulary statistics"""
    st.markdown("### 📊 Vocabulary Statistics")

    stats = vocab_learner.get_vocabulary_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Words", stats['total_words'])
    with col2:
        st.metric("Mastered", stats['mastered'])
    with col3:
        st.metric("Accuracy", f"{stats['accuracy']:.0f}%")

    # Words by level
    st.markdown("#### 📈 Words by CEFR Level")
    level_data = stats['by_level']
    for level in ['A1', 'A2', 'B1', 'B2']:
        count = level_data.get(level, 0)
        st.progress(count / max(stats['total_words'], 1), text=f"{level}: {count} words")

    # Difficult words
    if stats['difficult_words']:
        st.markdown("#### 😅 Words Needing Practice")
        for word in stats['difficult_words']:
            accuracy = (word['times_correct'] / word['times_seen'] * 100) if word['times_seen'] > 0 else 0
            st.markdown(f"- **{word['word']}** ({accuracy:.0f}% accuracy)")


def render_stats_page():
    """Render statistics page"""
    st.title("📊 Your Learning Statistics")

    # Overall stats
    stats = db.get_user_stats()
    level_info = xp_system.get_current_level_info()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Level", f"{level_info['current_level']} ({level_info['cefr_level']})")
    with col2:
        hours = stats['total_seconds_studied'] / 3600
        st.metric("Total Study Time", f"{hours:.1f} hours")
    with col3:
        st.metric("Total XP", f"{level_info['current_xp']:,}")

    st.markdown("### More stats coming soon!")
    st.info("Otto is working hard to bring you detailed analytics! 📈")


def render_achievements_page():
    """Render achievements page"""
    st.title("🏆 Achievements")

    achievements = db.get_achievements()
    unlocked = [a for a in achievements if a['unlocked']]
    locked = [a for a in achievements if not a['unlocked']]

    st.markdown(f"### Unlocked: {len(unlocked)}/{len(achievements)}")

    # Show unlocked achievements
    if unlocked:
        for ach in unlocked:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"## {ach['icon']}")
                with col2:
                    st.markdown(f"**{ach['title']}** ✅")
                    st.caption(ach['description'])
                    st.caption(f"Unlocked: {ach['unlocked_at'][:10] if ach['unlocked_at'] else 'Unknown'}")

    st.divider()

    # Show locked achievements with progress
    st.markdown("### 🔒 Locked Achievements")
    for ach in locked:
        progress_pct = (ach['progress'] / ach['requirement_value'] * 100) if ach['requirement_value'] > 0 else 0
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"## {ach['icon']}")
            with col2:
                st.markdown(f"**{ach['title']}** 🔒")
                st.caption(ach['description'])
                st.progress(min(progress_pct / 100, 1.0), text=f"{ach['progress']}/{ach['requirement_value']}")


def render_conversation_page():
    """Render conversation practice page"""
    st.title("💬 Conversation Partner")
    st.markdown("### Practice German conversation with Otto!")

    # Check if Ollama is available
    ollama_available = llm.check_ollama_installed()
    if not ollama_available:
        st.warning("⚠️ Ollama not detected. Using mock responses for demonstration.")
        st.info("📥 Install Ollama from https://ollama.ai for full AI-powered conversations!")

    # Select CEFR level
    cefr_level = st.selectbox(
        "Choose your level:",
        ["A1", "A2", "B1", "B2"],
        index=0,
        help="Select your German proficiency level"
    )

    # Get available scenarios for this level
    scenarios = conversation_manager.get_scenarios_by_level(cefr_level)

    if not scenarios:
        st.info(f"No scenarios available for {cefr_level} level yet. Check back soon!")
        return

    # Display scenarios
    st.markdown("#### Choose a scenario:")

    # Scenario selection
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = None
        st.session_state.conversation_active = False

    if not st.session_state.conversation_active:
        # Show scenario cards
        for scenario in scenarios:
            with st.expander(f"{scenario['name']}", expanded=False):
                st.markdown(f"**{scenario['description']}**")
                st.markdown(f"🎭 Otto's role: {scenario['otto_role']}")
                st.markdown(f"📍 Setting: {scenario['setting']}")
                st.markdown(f"🎯 Learn: {', '.join(scenario['learning_goals'])}")

                if st.button(f"Start '{scenario['name']}'", key=f"start_{scenario['id']}"):
                    # Start conversation
                    result = conversation_manager.start_scenario(scenario['id'], cefr_level)
                    st.session_state.selected_scenario = scenario
                    st.session_state.conversation_active = True
                    st.session_state.conversation_messages = []
                    st.rerun()

    else:
        # Active conversation
        scenario = st.session_state.selected_scenario

        st.success(f"🎭 Scenario: {scenario['name']}")
        st.info(f"📍 {scenario['setting']}")

        # Display conversation history
        st.markdown("### Conversation:")

        history = conversation_manager.get_conversation_history()

        for msg in history:
            if msg['role'] == 'otto':
                st.markdown(f"**🤖 Otto:** {msg['text']}")
            else:
                st.markdown(f"**👤 You:** {msg['text']}")

        # User input
        st.markdown("---")
        user_input = st.text_input(
            "Your response (in German):",
            key="user_conv_input",
            placeholder="Type your response in German..."
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button("Send", type="primary", use_container_width=True):
                if user_input.strip():
                    # Add user message
                    conversation_manager.add_user_message(user_input)

                    # Generate Otto's response
                    prompt = conversation_manager.build_conversation_prompt(user_input)
                    otto_response = llm.generate_conversation_response(prompt, use_mistral=True)

                    if otto_response:
                        conversation_manager.add_otto_message(otto_response)

                    # Clear input and rerun
                    st.rerun()

        with col2:
            if st.button("End Conversation", use_container_width=True):
                # End conversation
                summary = conversation_manager.end_conversation()

                st.session_state.conversation_active = False
                st.session_state.selected_scenario = None

                # Show summary
                st.success("🎉 Conversation complete!")
                st.markdown(f"**Messages exchanged:** {summary.get('total_messages', 0)}")
                st.markdown(f"**Your messages:** {summary.get('user_messages', 0)}")

                # Award XP (placeholder - integrate with xp_system later)
                st.info("💫 +50 XP for conversation practice!")

                st.rerun()

        # Show corrections sidebar if any
        corrections = conversation_manager.get_corrections()
        if corrections:
            with st.sidebar:
                st.markdown("### 📝 Corrections")
                for correction in corrections:
                    st.warning(f"**You said:** {correction['user_text']}")
                    st.success(f"**Better:** {correction['corrected_text']}")
                    st.info(f"💡 {correction['explanation']}")


def main():
    """Main application entry point"""
    # Render sidebar
    render_sidebar()

    # Render current page
    if st.session_state.page == 'home':
        render_home_page()
    elif st.session_state.page == 'vocabulary':
        render_vocabulary_page()
    elif st.session_state.page == 'conversation':
        render_conversation_page()
    elif st.session_state.page == 'stats':
        render_stats_page()
    elif st.session_state.page == 'achievements':
        render_achievements_page()


if __name__ == "__main__":
    main()
