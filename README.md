🧠 AI WebApp Builder Agent

An AI-powered, multi-agent system that converts natural language prompts into fully functional web applications. The system automatically generates HTML, CSS, and JavaScript, maps dependencies, applies modern styling, and can run the web app locally using agent orchestration.


🚀 Features

Prompt-based web app generation
Multi-agent architecture (HTML, CSS, JS, Run Agent)
Automatic dependency mapping in HTML
Modern, responsive UI styling
Human-in-the-loop confirmations
Local web server execution in a new terminal
Single-file implementation (app.py)


🏗️ Architecture Overview

User Prompt
   ↓
WebApp Builder Agent
   ├── HTML Agent (structure + dependencies)
   ├── CSS Agent (modern styling)
   ├── JavaScript Agent (interactivity)
   └── Run Agent (local server execution)


🛠️ Requirements

Python 3.9 or higher
agentapps library
Install dependencies:
pip install agentapps


▶️ How to Run

python app.py   
