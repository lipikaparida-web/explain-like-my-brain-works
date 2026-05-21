## Agent-orchestrator
A modular AI agent that uses LLM reasoning to select and execute tools dynamically in real time — demonstrating tool-calling, structured JSON outputs, and autonomous agent orchestration.
Built with Groq for fast LLM inference.

## What This Does
Most AI demos just call an LLM and print the response. This project goes a step further: the LLM decides which tool to use, executes it, and returns a structured result — the same core loop behind systems like AutoGPT, LangChain agents, and OpenAI function calling.
User Input → LLM Agent → Tool Selection → Tool Execution → Structured Output

## Features

LLM-driven intent understanding and tool selection
Dynamic tool dispatch at runtime
Structured JSON outputs for every response
Retry mechanism for robustness on transient failures
Modular design — add new tools in tools.py without touching agent logic
Simple CLI interface


## Project Structure
agent-orchestrator/
├── agent.py      # Core agent logic — LLM calls + tool decision making
├── tools.py      # Tool implementations (calculator, weather)
├── utils.py      # Retry mechanism and helpers
├── main.py       # CLI entry point
├── .env.example
└── requirements.txt

## Setup
1. Clone the repository
bashgit clone https://github.com/lipikaparida-web/agent-orchestrator.git
cd agent-orchestrator
2. Create a virtual environment
bashpython -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
3. Install dependencies
bashpip install -r requirements.txt
4. Add your API key
bashcp .env.example .env
Edit .env:
envGROQ_API_KEY=your_groq_api_key_here
Get a free key at console.groq.com.
5. Run the agent
bashpython main.py

## Example Interactions
Calculator tool
> Input:  2 + 3 * 10
  Output: 32
Weather tool
> Input:  weather in Chennai
  Output:
  {
    "city": "Chennai",
    "temperature": "30°C",
    "condition": "Sunny"
  }

## How It Works

User enters a natural language query via CLI
The LLM analyzes the intent and selects the appropriate tool
The agent calls that tool with extracted parameters
The result is returned as structured JSON
If the call fails, the retry mechanism in utils.py re-attempts before surfacing an error

The agent loop in agent.py keeps the LLM reasoning and tool execution cleanly separated — the LLM never directly executes anything, it only decides.

Available Tools
ToolTriggerDescriptioncalculatorMath expressionsEvaluates arithmetic safelyweather"weather in [city]"Returns mock weather for any city
Adding a new tool takes ~10 lines in tools.py — no changes needed elsewhere.

## Roadmap

 Web search tool
 File / document reader tool
 Conversational memory across turns
 Multi-step chain-of-thought execution
 Deploy as a REST API


## Tech Stack

Python 3.10+
Groq API — fast LLM inference (LLaMA 3 / Mixtral)
python-dotenv — credential management


## Author

**Lipika Parida** — [GitHub](https://github.com/lipikaparida-web) · [LinkedIn](https://www.linkedin.com/in/lipikaparida3/)
