# ClawCoder

Multi-language AI code generator supporting 39 programming languages with A2A routing, compiler validation, code translation, and project scaffolding.

## Features

- **Code Generation**: 39 languages with automatic language detection
- **Compiler Validation**: Syntax check for Python, Rust, Go, JavaScript, TypeScript
- **Code Translation**: Translate between languages with validation
- **Project Scaffolding**: Generate multi-file project structures
- **Code Execution**: Run generated code directly
- **Test Runner**: Execute test suites
- **Documentation**: Auto-generate docstrings and API docs
- **Performance Analysis**: Identify bottlenecks and optimizations
- **Dependency Management**: Generate requirements.txt, Cargo.toml, package.json
- **Project Scanning**: Analyze codebase structure and patterns

## Setup

```bash
pip install requests  # already in project requirements
Start the A2A server, connect to claw_coder from the menu, and type /help.

Commands
Command	Description
/code <task>	Generate code, auto-save with validation
/translate <from> <to> <file>	Translate code between languages
/run <lang> <file>	Execute code and show output
/test <lang> <file>	Run test suite
/scan structure	Show project tree
/scan patterns <lang>	Extract coding patterns
/scan <query>	Full project context for query
/docs <lang> <file>	Generate documentation
/docs <lang> --all	List available files for a language
/project <lang> <fw> <name>	Scaffold multi-file project
/deps <lang> <pkgs>	Generate dependency file
/perf <lang> <file>	Performance analysis
/explain <topic>	Explain programming concepts
/debug <code>	Debug and fix issues
/review <code>	Code review with improvements
/tutorial <topic>	Step-by-step tutorial
/find <query>	Search web for programming resources
/help	Show help
/stats	Show interaction statistics
Code Translation
bash
/translate python rust python_async_web_scraper.py
/translate python go myfile.py
/translate python javascript python_fibonacci_function.py
Output is validated against the target language compiler when available.

Code Generation with Scan
bash
/code --scan add a new endpoint for user authentication
The --scan flag reads your project structure and generates code matching your existing patterns.

Supported Languages (39)
Python, Rust, Go, JavaScript, TypeScript, Java, C, C++, C#, Ruby, PHP, Swift, Kotlin, Scala, R, Julia, Lua, Perl, Haskell, Clojure, Elixir, Erlang, Dart, Bash, PowerShell, SQL, HTML, CSS, YAML, JSON, XML, Assembly, Fortran, COBOL, Groovy, Nim, Zig, MATLAB, Makefile

File Structure
text
agents/claw_coder/
├── agent_handler.py          # A2A handler with full command routing
├── commands/
│   ├── run.py                # Code execution
│   ├── test.py               # Test runner
│   ├── translate.py          # Code translation
│   ├── docs.py               # Documentation generator
│   ├── project.py            # Project scaffolding
│   ├── deps.py               # Dependency management
│   └── perf.py               # Performance analysis
├── engine/
│   └── scanner.py            # Project scanner
├── languages/                # Language definitions
└── utils/                    # Utility functions
A2A Integration
python
self.call_agent("claw_coder", "/code python async web scraper")
self.call_agent("claw_coder", "/translate python rust myfile.py")
Troubleshooting
"LLMClaw unavailable": Ensure A2A server is running

Slow responses: Switch models via LLMClaw — /use gemma3:12b

Wrong language detected: Specify explicitly — /code rust async TCP server

Compiled not found: Install the language toolchain — Python, Rust, Go, Node.js