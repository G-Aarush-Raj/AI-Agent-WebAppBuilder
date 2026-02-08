import os
import sys
import subprocess
from agentapps import Agent, Tool
from agentapps.model import GrokChat

# =====================================================
# 1️⃣ MODEL
# =====================================================

grok_model = GrokChat(
    id="grok-3-mini",
    api_key="GROK-API-KEY"
)

# =====================================================
# 2️⃣ TOOLS (NO AI LOGIC)
# =====================================================

class CreateWebAppTool(Tool):
    def __init__(self):
        super().__init__(
            name="create_webapp",
            description="Create a web app folder with HTML, CSS, and JS files"
        )

    def execute(self, project_name: str, html_code: str, css_code: str, js_code: str) -> str:
        folder = project_name.replace(" ", "_").lower()
        os.makedirs(folder, exist_ok=True)

        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(html_code)
        open(os.path.join(folder, "styles.css"), "w", encoding="utf-8").write(css_code)
        open(os.path.join(folder, "script.js"), "w", encoding="utf-8").write(js_code)

        return f"Web app created in folder: {folder}"

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "html_code": {"type": "string"},
                "css_code": {"type": "string"},
                "js_code": {"type": "string"}
            },
            "required": ["project_name", "html_code", "css_code", "js_code"]
        }


class RunWebAppTool(Tool):
    def __init__(self):
        super().__init__(
            name="run_webapp",
            description="Run the generated web app in a new terminal window"
        )

    def execute(self, project_name: str, port: int = 8000) -> str:
        folder = project_name.strip().lower()

        if not os.path.isdir(folder):
            return f"Project folder '{folder}' not found."

        # Windows: open a NEW command prompt window
        command = (
            f'start cmd /k "cd /d {os.path.abspath(folder)} '
            f'&& python -m http.server {port}"'
        )

        subprocess.Popen(command, shell=True)

        return f"Web app is running in a new terminal at http://localhost:{port}"

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "port": {"type": "integer"}
            },
            "required": ["project_name"]
        }


# =====================================================
# 3️⃣ GENERATION AGENTS
# =====================================================

html_agent = Agent(
    name="HTML Agent",
    role="Generate HTML with strict dependency mapping",
    model=grok_model,
    instructions=[
        "Generate a complete index.html file",
        "ALWAYS use standard HTML5 boilerplate",
        "ALWAYS link local CSS as: <link rel='stylesheet' href='style.css'>",
        "ALWAYS link local JS as: <script src='script.js' defer></script>",
        "Include modern external dependencies when useful:",
        "- Google Fonts (Inter or Poppins)",
        "- modern-normalize CSS reset",
        "Do NOT embed CSS or JS inline",
        "Ensure semantic, accessible HTML",
        "Follow the exact filenames provided style.css ONLY"
    ]
)


css_agent = Agent(
    name="CSS Agent",
    role="Generate modern CSS styling",
    model=grok_model,
    instructions=[
        "Generate a complete style.css file",
        "Use modern design principles:",
        "- CSS variables for colors",
        "- Flexbox or Grid for layout",
        "- Smooth hover and transition effects",
        "- Consistent spacing and typography",
        "Use a clean color palette suitable for production UI",
        "Ensure responsive design for mobile and desktop",
        "Avoid inline styles",
        "Make the UI visually appealing and professional"
    ]
)


js_agent = Agent(
    name="JavaScript Agent",
    role="Generate JavaScript logic",
    model=grok_model,
    instructions=[
        "Generate a clean and functional script.js file",
        "Ensure all DOM elements are accessed after page load",
        "Add meaningful interactivity relevant to the app",
        "Avoid unsafe practices unless necessary",
        "Keep code readable and well-structured"
    ]
)

run_agent = Agent(
    name="Run Agent",
    role="Run website",
    model=grok_model,
    tools=[RunWebAppTool()],
    instructions=["Run the website using the project name"]
)

# =====================================================
# 4️⃣ BUILDER AGENT (FULL CONTROL)
# =====================================================

builder_agent = Agent(
    name="WebApp Builder Agent",
    team=[html_agent, css_agent, js_agent, run_agent],
    tools=[CreateWebAppTool()],
    model=grok_model,
    instructions=[
        "You manage a multi-step conversation for building and running a web app.",

        "When the user gives a full request (e.g. 'Build a calculator app'), you must:",
        "- Derive a project_name (e.g. calculator_app)",
        "- Build the web app using create_webapp",
        "- Remember this project_name for the entire conversation",

        "After building, ASK exactly:",
        "'Do you want me to run the web app?'",

        "IMPORTANT CONFIRMATION LOGIC:",
        "- If the user replies 'Yes', 'yes', 'Y', or 'y',",
        "  treat it as confirmation to RUN the LAST CREATED project",
        "  using the SAME project_name.",
        "- Do NOT ask for a new project description in this case.",

        "- If the user replies 'No', 'no', 'N', or 'n',",
        "  do NOT run the web app and end the flow politely.",

        "After running the web app, ASK:",
        "'Do you want any modifications?'",

        "- If the user replies with modification details, rebuild the app",
        "  using the SAME project_name.",
        "- If the user replies 'No', confirm completion.",

        "NEVER treat 'Yes' or 'No' as a new build request.",
        "NEVER ask for clarification when the user replies with Yes/No.",
        "Always act based on the last pending question."
    ],
    show_tool_calls=True
)




# =====================================================
# 5️⃣ MINIMAL LOOP (AGENT-DRIVEN)
# =====================================================

if __name__ == "__main__":
    print("🚀 WebApp Builder Agent")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ("exit", "quit"):
            break

        response = builder_agent.print_response(user_input)
        print(response)
