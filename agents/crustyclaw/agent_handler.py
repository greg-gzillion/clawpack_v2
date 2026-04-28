"""A2A Handler for CrustyClaw - Rust AI with compiler validation + standalone bridge"""
import sys, os, subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CRUSTY_DIR = Path(__file__).resolve().parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CRUSTY_DIR))

from shared.base_agent import BaseAgent

class CrustyClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("crustyclaw")
        self.cargo_path = str(Path.home() / "dev")

    def _validate_rust(self, filepath):
        """Validate Rust code with rustc."""
        try:
            result = subprocess.run(
                ["rustc", "--edition", "2024", "--emit=metadata", str(filepath)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return "Compilation OK"
            return result.stderr[:200] if result.stderr else "Compilation failed"
        except FileNotFoundError:
            return "rustc not installed"
        except Exception as e:
            return str(e)

    def _run_standalone(self, command, args=""):
        """Bridge to the standalone crustyclaw binary if available."""
        binary_paths = [
            CRUSTY_DIR / "target" / "release" / "crustyclaw.exe",
            CRUSTY_DIR / "target" / "release" / "crustyclaw",
            Path.home() / ".cargo" / "bin" / "crustyclaw",
        ]
        for binary in binary_paths:
            if binary.exists():
                try:
                    cmd = [str(binary), command]
                    if args:
                        cmd.append(args)
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    return result.stdout or result.stderr
                except:
                    pass
        return None

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/rust", "/code") and query:
                result = self.ask_llm(f"Write clean Rust 2024 edition code. Return only the code with brief comments. Task: {query}")
                code = result
                if "```" in code:
                    blocks = code.split("```")
                    for i, block in enumerate(blocks):
                        if i % 2 == 1:
                            block = block.split("\n", 1)[1] if "\n" in block else block
                            code = block
                            break
                name = query.replace(" ", "_").replace("\\", "").replace("/", "")[:50]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"{name}_{ts}.rs"
                filepath = EXPORTS / fn
                EXPORTS.mkdir(exist_ok=True)
                filepath.write_text(code, encoding="utf-8")
                validation = self._validate_rust(filepath)
                result = f"Saved: {fn} | Validated: {validation}\n\n{result}"

            elif cmd in ("/explain",) and query:
                result = self.ask_llm(f"Explain this Rust concept clearly with code examples: {query}")

            elif cmd == "/cargopath" and not args:
                result = f"Current cargo path: {self.cargo_path}\nUsage: /cargopath ~/dev/my-rust-project"
            elif cmd == "/cargopath" and query:
                new_path = Path(query).expanduser().resolve()
                if new_path.exists():
                    self.cargo_path = str(new_path)
                    result = f"Cargo path set to: {self.cargo_path}"
                else:
                    result = f"Path not found: {new_path}"

            elif cmd in ("/cargo",) and query:
                allowed = {"build", "check", "test", "run", "clean", "doc", "fmt", "clippy", "bench", "update", "version", "help"}
                parts_cmd = query.split()
                if not parts_cmd or parts_cmd[0] not in allowed:
                    result = f"Allowed cargo commands: {sorted(allowed)}"
                else:
                    try:
                        cargo_result = subprocess.run(
                            ["cargo"] + parts_cmd,
                            capture_output=True, text=True, timeout=60,
                            cwd=self.cargo_path
                        )
                        result = cargo_result.stdout or cargo_result.stderr or "Cargo completed"
                    except Exception as e:
                        result = f"Cargo error: {e}"

            elif cmd in ("/audit",) and query:
                standalone = self._run_standalone("audit", query)
                if standalone:
                    result = f"[Standalone audit]\n{standalone}"
                else:
                    result = self.ask_llm(f"Security audit this Rust code. Check for: unsafe blocks, unwrap usage, input validation, dependency vulnerabilities, memory safety. Code:\n{query[:4000]}")

            elif cmd in ("/pinch",) and query:
                standalone = self._run_standalone("pinch", query)
                if standalone:
                    result = f"[Standalone pinch]\n{standalone}"
                else:
                    result = self.ask_llm(f"Analyze this Rust code for unnecessary clones, inefficient allocations, and optimization opportunities. Code:\n{query[:4000]}")

            elif cmd in ("/fix", "/debug") and query:
                result = self.ask_llm(f"Debug and fix this Rust code. Show the corrected version: {query[:4000]}")

            elif cmd in ("/test",) and query:
                result = self.ask_llm(f"Write comprehensive Rust unit tests with #[cfg(test)] for this code: {query[:4000]}")

            elif cmd in ("/run",):
                try:
                    run_result = subprocess.run(
                        ["cargo", "run"],
                        capture_output=True, text=True, timeout=30,
                        cwd=self.cargo_path
                    )
                    result = run_result.stdout or run_result.stderr or "Program completed"
                except Exception as e:
                    result = f"Run error: {e}"

            elif cmd == "/help":
                result = """CrustyClaw - Rust AI Assistant
  /rust /code <task>   - Generate Rust + validate + auto-save
  /explain <concept>   - Explain Rust concepts
  /cargopath <path>    - Set cargo working directory
  /cargo <cmd>         - Run cargo (build, check, test, fmt, clippy)
  /audit <code>        - Security audit (uses standalone binary if available)
  /pinch <path>        - Detect unnecessary clones (uses standalone binary)
  /fix /debug <code>   - Debug and fix Rust code
  /test <code>         - Generate unit tests
  /run                 - cargo run in current cargo path
  /help /stats"""

            elif cmd == "/stats":
                result = f"CrustyClaw | Rust AI | Compiler Validation | Standalone Bridge | Cargo: {self.cargo_path} | Interactions: {self.state.get('interactions', 0)}"

            elif query:
                result = self.ask_llm(f"Rust expert. Question: {query}")
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = CrustyClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)