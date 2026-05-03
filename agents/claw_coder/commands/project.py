def run(args):
    """Scaffold a multi-file project. Usage: /project python fastapi todo-api"""
    if not args:
        return "Usage: /project python fastapi todo-api\n       /project rust cli tool-name\n       /project go web-server project-name"

    parts = args.split(maxsplit=2)
    lang = parts[0].lower()
    framework = parts[1].lower() if len(parts) > 1 else ""
    name = parts[2] if len(parts) > 2 else "my-project"

    from pathlib import Path
    from agent_handler import _agent

    PROJECT_ROOT = Path("str(PROJECT_ROOT)")
    EXPORTS = PROJECT_ROOT / "exports" / name

    prompt = f"""Create a complete {lang} project using {framework}.
Project name: {name}

Generate ALL files needed for a working project. Return as a structured list with file paths and content:

=== FILE STRUCTURE ===
exports/{name}/
├── README.md
├── requirements.txt
├── src/
│   ├── main file
│   ├── config
│   ├── models
│   └── routes (or handlers)
└── tests/
    └── test_main

For each file, provide:
FILE: path/to/file
<file content>
"""
    
    result = _agent.ask_llm(prompt)
    return f"Project scaffold for {name}:\n\n{result}"