"""
=============================================================
  Explain Like My Brain Works
  AMD Slingshot Hackathon 2026 — AI in Education & Skilling
=============================================================
  A personalized AI learning assistant that explains any topic
  in the student's preferred learning style, then quizzes them.

  Tech: Python + Streamlit
  AI: Anthropic Claude (via API) with mock fallback for demo
=============================================================
"""

import streamlit as st
import random

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Explain Like My Brain Works",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — clean, modern, student-friendly design
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

    /* Root variables */
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #43D9AD;
        --bg: #0F0F1A;
        --card: #1A1A2E;
        --text: #E8E8F0;
        --muted: #8888AA;
    }

    /* Global overrides */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Hero header */
    .hero {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
    }
    .hero h1 {
        font-family: 'Sora', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6C63FF, #43D9AD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: var(--muted);
        font-size: 1.05rem;
    }

    /* Style pill badges for learning styles */
    .style-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .badge-visual    { background: #6C63FF22; color: #A89CFF; border: 1px solid #6C63FF44; }
    .badge-step      { background: #43D9AD22; color: #43D9AD; border: 1px solid #43D9AD44; }
    .badge-analogy   { background: #FF658422; color: #FF9AAF; border: 1px solid #FF658444; }

    /* Explanation card */
    .explanation-card {
        background: var(--card);
        border: 1px solid #2A2A4A;
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        line-height: 1.75;
        font-size: 1.02rem;
    }

    /* Quiz question card */
    .quiz-card {
        background: var(--card);
        border: 1px solid #2A2A4A;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 1rem 0;
    }
    .quiz-card .q-num {
        font-family: 'Sora', sans-serif;
        font-size: 0.78rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }
    .quiz-card .q-text {
        font-weight: 600;
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
        color: var(--text);
    }

    /* Feedback banners */
    .feedback-correct {
        background: #43D9AD18;
        border-left: 4px solid #43D9AD;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-top: 0.4rem;
        color: #43D9AD;
        font-weight: 500;
    }
    .feedback-wrong {
        background: #FF658418;
        border-left: 4px solid #FF6584;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-top: 0.4rem;
        color: #FF9AAF;
        font-weight: 500;
    }

    /* Score summary box */
    .score-box {
        text-align: center;
        background: linear-gradient(135deg, #6C63FF22, #43D9AD22);
        border: 1px solid #6C63FF44;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    .score-box .score-num {
        font-family: 'Sora', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #A89CFF;
    }
    .score-box .score-label {
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #2A2A4A;
        margin: 2rem 0;
    }

    /* Section headers */
    .section-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin: 1.5rem 0 0.5rem;
    }

    /* Streamlit widget label color fix */
    .stSelectbox label, .stTextInput label, .stRadio label {
        color: var(--muted) !important;
        font-size: 0.9rem !important;
    }

    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF, #8A84FF);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.88;
    }

    /* Info box */
    .info-tip {
        background: #1E1E35;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MOCK DATA — realistic placeholder responses for demo purposes
# Replace the body of each function with a real LLM API call
# ─────────────────────────────────────────────────────────────

# Each key maps a (learning_style) to a template explanation.
# For the prototype, we use rich placeholder text that mimics
# what a real LLM would return.

MOCK_EXPLANATIONS = {
    "Visual 🎨": """
🖼️ **Picture This — A Visual Breakdown**

Imagine **{topic}** as a living map you can walk through.

```
┌──────────────────────────────────────────┐
│              {topic}                     │
│                                          │
│   [Core Idea] ──► [How it works]         │
│        │                │                │
│        ▼                ▼                │
│   [Why it matters]  [Real example]       │
└──────────────────────────────────────────┘
```

**The Big Picture 🌍**
Think of {topic} as a system of interconnected nodes. Each piece feeds into the next. When you zoom out, you see the full shape — like satellite view of a city's roads.

**The Layers 📦**
- **Layer 1 (Foundation):** The most basic version of the idea — the "what"
- **Layer 2 (Mechanics):** How the pieces interact — the "how"  
- **Layer 3 (Impact):** What changes because this exists — the "so what"

**Color-code it mentally:**
🔵 Blue = definitions  |  🟡 Yellow = process  |  🟢 Green = examples

Visual learners: try sketching this as a mind-map after reading!
""",

    "Step-by-Step 🪜": """
🪜 **Step-by-Step Breakdown of {topic}**

Let's break this down into clean, ordered steps — no skipping ahead!

---

**Step 1 — Start with the "Why"**
Before anything, ask: *Why does {topic} exist?* Every concept was born to solve a problem. Understanding the problem makes the solution 10× clearer.

**Step 2 — Define the Core Terms**
Write down the 3–5 key words that keep appearing. These are the vocabulary of {topic}. You can't skip this — it's like trying to read without knowing the alphabet.

**Step 3 — Understand the Mechanism**
Now ask: *How does it work?* Walk through the process in order. If A happens, then B follows, and C results. Trace the chain.

**Step 4 — Find a Small Example**
Take the simplest case you can think of and apply {topic} to it. Start tiny. Once that works, scale up.

**Step 5 — Test Your Understanding**
Try to explain {topic} out loud to an imaginary friend in under 60 seconds. If you stumble, go back to the step where you lost confidence.

**Step 6 — Connect to What You Know**
Where does {topic} appear in things you've already learned? This "hook" locks it into long-term memory.

---
✅ You now have a repeatable framework you can apply to *any* new topic!
""",

    "Real-life Analogy 🌍": """
🌍 **{topic} — But Make It Relatable**

> *"If you can't explain it simply, you don't understand it well enough."* — Often attributed to Einstein

---

**The Analogy 🎯**

Think about how a **city's traffic system** works.

- There are *roads* (the structure)
- *Cars* following rules (the agents)
- *Traffic lights* controlling flow (the rules/logic)
- And a *destination* everyone is trying to reach (the goal)

**{topic} works the same way.**

The "roads" of {topic} are its foundational structure — they determine what's possible. The "cars" are the data, energy, or information moving through it. The "traffic lights" are the constraints and rules that keep everything from becoming chaos. And the "destination" is the output or result the whole system is designed to produce.

---

**Another way to see it 🎬**

Imagine you're a chef making a complex dish. You don't throw everything in at once — you follow a *recipe* with timing and sequence. {topic} has the same logic: sequence matters, quantities matter, and the final product depends on how well you followed the process.

---

**Why this matters in real life 🏙️**
Next time you see {topic} mentioned — in a textbook, a news article, or a conversation — you'll recognize its shape. You've already met it in everyday life. You just didn't know what it was called.
""",
}

# ─────────────────────────────────────────────────────────────
# Mock quiz questions keyed by learning style
# ─────────────────────────────────────────────────────────────
MOCK_QUIZZES = {
    "Visual 🎨": [
        {
            "question": "When visualizing {topic}, which layer represents the foundational 'what'?",
            "options": ["Layer 3 (Impact)", "Layer 2 (Mechanics)", "Layer 1 (Foundation)", "The Satellite View"],
            "answer": "Layer 1 (Foundation)",
            "explanation": "Layer 1 is the starting point — the core definition before any process or impact is explored.",
        },
        {
            "question": "In the visual map of {topic}, what does the 🟢 Green color-code represent?",
            "options": ["Definitions", "Processes", "Examples", "Warnings"],
            "answer": "Examples",
            "explanation": "Green = Examples. Color-coding helps visual learners categorize information at a glance.",
        },
        {
            "question": "Why is 'zooming out' useful when studying {topic} visually?",
            "options": [
                "It hides confusing details",
                "It shows how all pieces connect in the big picture",
                "It makes the topic seem simpler than it is",
                "It replaces the need to read",
            ],
            "answer": "It shows how all pieces connect in the big picture",
            "explanation": "A high-level view (like satellite view) reveals relationships between parts that are invisible up close.",
        },
    ],
    "Step-by-Step 🪜": [
        {
            "question": "According to the step-by-step method, what should you do FIRST when learning {topic}?",
            "options": ["Memorize definitions", "Understand the 'Why'", "Find examples", "Test yourself"],
            "answer": "Understand the 'Why'",
            "explanation": "Step 1 is always the 'Why' — understanding the problem a concept solves makes everything else click.",
        },
        {
            "question": "In Step 5, what is the recommended way to test your understanding of {topic}?",
            "options": [
                "Write a 10-page essay",
                "Take a multiple choice exam",
                "Explain it out loud in under 60 seconds",
                "Search it on the internet",
            ],
            "answer": "Explain it out loud in under 60 seconds",
            "explanation": "The 'teach-back' method (Feynman Technique) is one of the most effective self-assessment tools.",
        },
        {
            "question": "Why does Step 6 ask you to connect {topic} to prior knowledge?",
            "options": [
                "To show off what you know",
                "To lock it into long-term memory",
                "To skip re-reading it later",
                "Because the teacher requires it",
            ],
            "answer": "To lock it into long-term memory",
            "explanation": "Connecting new ideas to existing knowledge creates stronger neural pathways — this is called elaborative encoding.",
        },
    ],
    "Real-life Analogy 🌍": [
        {
            "question": "In the city traffic analogy for {topic}, what do the 'traffic lights' represent?",
            "options": ["The goal/output", "The rules and constraints", "The structure/roads", "The data flowing through"],
            "answer": "The rules and constraints",
            "explanation": "Traffic lights control flow and prevent chaos — just like rules/logic govern how {topic} operates.",
        },
        {
            "question": "What does the 'chef following a recipe' analogy highlight about {topic}?",
            "options": [
                "That it tastes good",
                "That creativity matters more than rules",
                "That sequence and precision are important",
                "That you need professional training",
            ],
            "answer": "That sequence and precision are important",
            "explanation": "The recipe analogy emphasizes that in {topic}, the *order* and *proportion* of steps matter — not just the ingredients.",
        },
        {
            "question": "What is the main benefit of learning {topic} through analogies?",
            "options": [
                "It replaces the need for technical study",
                "It makes you recognize the concept in everyday life",
                "It is faster than reading textbooks",
                "It is only useful for visual learners",
            ],
            "answer": "It makes you recognize the concept in everyday life",
            "explanation": "Analogies bridge abstract concepts to lived experience — making recognition and recall much easier.",
        },
    ],
}


# ─────────────────────────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────────────────────────

def get_explanation(topic: str, style: str) -> str:
    """
    Generate a personalized explanation for a given topic and learning style.

    In a production app, replace the body of this function with:
        response = anthropic_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    Args:
        topic: The subject the student wants to learn about.
        style: One of the three learning styles.

    Returns:
        A formatted explanation string.
    """
    # Fetch the template for the chosen style and inject the topic
    template = MOCK_EXPLANATIONS.get(style, MOCK_EXPLANATIONS["Step-by-Step 🪜"])
    return template.replace("{topic}", topic)


def get_quiz(topic: str, style: str) -> list[dict]:
    """
    Generate 3 MCQ questions relevant to the topic and style.

    In production, send the explanation to the LLM and ask it to
    generate quiz questions with options and correct answers as JSON.

    Args:
        topic: The subject the student learned about.
        style: The learning style used — quiz questions match the style.

    Returns:
        A list of 3 question dicts with keys:
            question, options, answer, explanation
    """
    questions = MOCK_QUIZZES.get(style, MOCK_QUIZZES["Step-by-Step 🪜"])

    # Inject the topic name into question text
    processed = []
    for q in questions:
        processed.append({
            "question": q["question"].replace("{topic}", f"**{topic}**"),
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q["explanation"].replace("{topic}", topic),
        })
    return processed


def score_message(score: int, total: int) -> tuple[str, str]:
    """
    Return an encouraging message and emoji based on the quiz score.

    Args:
        score: Number of correct answers.
        total: Total number of questions.

    Returns:
        A tuple of (emoji, message).
    """
    pct = score / total
    if pct == 1.0:
        return "🏆", "Perfect score! You've truly understood this topic."
    elif pct >= 0.67:
        return "🌟", "Great job! A little review will make you unstoppable."
    elif pct >= 0.33:
        return "💪", "Good effort! Re-read the explanation and try again."
    else:
        return "📚", "Keep going! Every expert was once a beginner."


# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# Streamlit re-runs the script on every interaction, so we use
# st.session_state to persist values across reruns.
# ─────────────────────────────────────────────────────────────
defaults = {
    "explanation": None,       # Generated explanation text
    "quiz": None,              # List of quiz question dicts
    "answers": {},             # User's selected answers {q_index: choice}
    "submitted": False,        # Whether the quiz has been submitted
    "topic": "",               # Last topic that was explained
    "style": "",               # Last style that was used
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─────────────────────────────────────────────────────────────
# UI — HERO HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧠 Explain Like My Brain Works</h1>
    <p>AI-powered explanations, tailored to <em>your</em> learning style</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# UI — INPUT SECTION
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What do you want to learn?</div>', unsafe_allow_html=True)

# Topic input — any subject the student is curious about
topic = st.text_input(
    label="Enter a topic",
    placeholder="e.g.  Photosynthesis, Binary Search, The French Revolution...",
    label_visibility="collapsed",
)

# Learning style selector
st.markdown('<div class="section-title">How does your brain like to learn?</div>', unsafe_allow_html=True)

style_options = list(MOCK_EXPLANATIONS.keys())
style = st.selectbox(
    label="Choose your learning style",
    options=style_options,
    help="Pick the style that resonates most with how you naturally understand things.",
    label_visibility="collapsed",
)

# Style descriptions shown below the dropdown
style_descriptions = {
    "Visual 🎨":          ("badge-visual",  "Diagrams, maps & colour-coded structures"),
    "Step-by-Step 🪜":    ("badge-step",    "Ordered steps, clear logic, no skipping"),
    "Real-life Analogy 🌍": ("badge-analogy","Everyday comparisons that click instantly"),
}
badge_class, badge_text = style_descriptions[style]
st.markdown(f'<span class="style-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# UI — GENERATE EXPLANATION BUTTON
# ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 3])
with col1:
    explain_btn = st.button("✨ Explain it!", use_container_width=True)

# When the button is clicked, validate inputs and generate explanation
if explain_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before generating an explanation.")
    else:
        with st.spinner("Crafting your personalized explanation..."):
            explanation = get_explanation(topic.strip(), style)

        # Store results in session state so they persist on rerun
        st.session_state.explanation = explanation
        st.session_state.quiz = None        # Reset quiz when new explanation is generated
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.topic = topic.strip()
        st.session_state.style = style


# ─────────────────────────────────────────────────────────────
# UI — EXPLANATION DISPLAY
# ─────────────────────────────────────────────────────────────
if st.session_state.explanation:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📖 Your {st.session_state.style} Explanation</div>', unsafe_allow_html=True)

    # Render the explanation inside a styled card
    st.markdown(
        f'<div class="explanation-card">{st.session_state.explanation}</div>',
        unsafe_allow_html=True,
    )
    # Note: the explanation uses markdown syntax, so we also render it natively
    # for proper bold/code formatting inside Streamlit
    with st.expander("📄 View clean formatted version", expanded=False):
        st.markdown(st.session_state.explanation)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # UI — GENERATE QUIZ BUTTON
    # ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🧩 Ready to test yourself?</div>', unsafe_allow_html=True)
    st.caption("3 quick questions to check how well the explanation landed.")

    quiz_btn = st.button("🎯 Generate Quiz", use_container_width=False)

    if quiz_btn:
        with st.spinner("Preparing your quiz..."):
            quiz = get_quiz(st.session_state.topic, st.session_state.style)

        st.session_state.quiz = quiz
        st.session_state.answers = {}
        st.session_state.submitted = False


# ─────────────────────────────────────────────────────────────
# UI — QUIZ DISPLAY
# ─────────────────────────────────────────────────────────────
if st.session_state.quiz:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Quick Quiz</div>', unsafe_allow_html=True)

    # Display each question as its own block
    for i, q in enumerate(st.session_state.quiz):
        st.markdown(
            f"""
            <div class="quiz-card">
                <div class="q-num">Question {i + 1} of {len(st.session_state.quiz)}</div>
                <div class="q-text">{q['question']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Radio buttons for answer choices
        # Disable once quiz is submitted so answers can't be changed
        selected = st.radio(
            label=f"q_{i}",
            options=q["options"],
            index=None,
            key=f"radio_{i}",
            disabled=st.session_state.submitted,
            label_visibility="collapsed",
        )

        # Track the user's selection in session state
        if selected:
            st.session_state.answers[i] = selected

        # Show per-question feedback after submission
        if st.session_state.submitted and i in st.session_state.answers:
            user_ans = st.session_state.answers[i]
            correct_ans = q["answer"]
            if user_ans == correct_ans:
                st.markdown(
                    f'<div class="feedback-correct">✅ Correct! {q["explanation"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="feedback-wrong">❌ Not quite. The correct answer is <strong>{correct_ans}</strong>. {q["explanation"]}</div>',
                    unsafe_allow_html=True,
                )

        st.write("")  # Spacing between questions

    # ─────────────────────────────────────────────────────────
    # UI — SUBMIT QUIZ BUTTON & SCORE
    # ─────────────────────────────────────────────────────────
    if not st.session_state.submitted:
        submit_btn = st.button("✅ Submit Answers", use_container_width=False)

        if submit_btn:
            answered_count = len(st.session_state.answers)
            total_q = len(st.session_state.quiz)

            # Make sure all questions are answered before submitting
            if answered_count < total_q:
                st.warning(f"⚠️ Please answer all {total_q} questions before submitting ({answered_count}/{total_q} answered).")
            else:
                st.session_state.submitted = True
                st.rerun()  # Re-render to show feedback state

    # Score summary — shown after submission
    if st.session_state.submitted:
        total_q = len(st.session_state.quiz)
        score = sum(
            1
            for i, q in enumerate(st.session_state.quiz)
            if st.session_state.answers.get(i) == q["answer"]
        )
        emoji, message = score_message(score, total_q)

        st.markdown(
            f"""
            <div class="score-box">
                <div style="font-size:2.5rem">{emoji}</div>
                <div class="score-num">{score}/{total_q}</div>
                <div class="score-label">{message}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Option to retry with a different style
        st.info("💡 Try a different learning style above to see if another explanation clicks even better!", icon="🔄")


# ─────────────────────────────────────────────────────────────
# UI — FOOTER TIP
# ─────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="info-tip">
    🚀 <strong>Hackathon Demo Note:</strong> This prototype uses rich mock responses.
    In production, replace <code>get_explanation()</code> and <code>get_quiz()</code>
    with real Anthropic Claude API calls for fully dynamic, topic-specific content.
</div>
""", unsafe_allow_html=True)
