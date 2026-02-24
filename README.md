# Explain Like My Brain Works
**AMD Slingshot Hackathon 2026 — AI in Education & Skilling**

> An AI learning assistant that explains any topic in your preferred style, then checks understanding with a short quiz.

---

## Quick Start

### 1. Clone / download the project
```bash
git clone <your-repo-url>
cd explain-like-my-brain-works
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## Project Structure

```
.
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Enabling Real AI (Production Mode)

The prototype ships with rich mock responses so it works out-of-the-box.
To connect real Claude AI:

1. Install the Anthropic SDK:
   ```bash
   pip install anthropic
   ```

2. Get your API key from https://console.anthropic.com

3. Export it as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

4. In `app.py`, replace the body of `get_explanation()` with:
   ```python
   import anthropic
   client = anthropic.Anthropic()

   style_prompts = {
       "Visual ": "Use visual metaphors, diagrams in ASCII, and structured layout.",
       "Step-by-Step ": "Break it into clearly numbered sequential steps.",
       "Real-life Analogy ": "Use a memorable real-world analogy a student can relate to.",
   }

   prompt = f"""Explain '{topic}' to a student using this style: {style_prompts[style]}.
   Keep the explanation clear, engaging, and under 300 words."""

   response = client.messages.create(
       model="claude-opus-4-6",
       max_tokens=800,
       messages=[{"role": "user", "content": prompt}]
   )
   return response.content[0].text
   ```

5. Similarly update `get_quiz()` to ask Claude to return JSON quiz questions.

---

## Features

| Feature | Status |
|---|---|
| Topic input | ✅ |
| Learning style selector (3 styles) | ✅ |
| Personalized explanation generation | ✅ (mock) |
| Quiz generation (3 MCQs) | ✅ (mock) |
| Answer selection UI | ✅ |
| Per-question feedback with explanation | ✅ |
| Score summary with encouragement | ✅ |
| Session state (no page reloads) | ✅ |
| Real Claude AI integration | plug-in ready |

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** — UI framework


---

*Built for AMD Slingshot Hackathon 2026*
