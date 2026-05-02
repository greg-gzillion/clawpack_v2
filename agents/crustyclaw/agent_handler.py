"""A2A Handler for CrustyClaw v5 - Constitutional Rust agent"""
import sys, os, json, subprocess
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
        try:
            result = subprocess.run(["rustc","--edition","2024","--emit=metadata",str(filepath)], capture_output=True, text=True, timeout=30)
            return "Compilation OK" if result.returncode==0 else result.stderr[:200]
        except FileNotFoundError: return "rustc not installed"
        except Exception as e: return str(e)

    def _run_standalone(self, command, args=""):
        binary_paths = [CRUSTY_DIR/"target"/"release"/"crustyclaw.exe", CRUSTY_DIR/"target"/"release"/"crustyclaw", Path.home()/".cargo"/"bin"/"crustyclaw"]
        for binary in binary_paths:
            if binary.exists():
                try:
                    cmd = [str(binary), command]; 
                    if args: cmd.append(args)
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    return result.stdout or result.stderr
                except: pass
        return None

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "CrustyClaw v5 - Constitutional Rust Agent\n  /rust /code <task>  /explain /audit /pinch /fix /test\n  /cargo <cmd>  /run\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}

            if cmd in ("/stats",):
                return {"status":"success","result":f"CrustyClaw v5 | Rust AI | Interactions: {self.state.get('interactions',0)}"}

            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","interpretclaw","docuclaw","dataclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/rust","/code") and query:
                result = self.ask_llm(f"Write clean Rust 2024 edition code. Return only the code with brief comments. Task: {query}")
                code = result
                if "`" in code:
                    blocks = code.split("`")
                    for i, block in enumerate(blocks):
                        if i%2==1:
                            block = block.split("\n",1)[1] if "\n" in block else block
                            code = block; break
                name = query.replace(" ","_").replace("\\","").replace("/","")[:50]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"{name}_{ts}.rs"
                filepath = EXPORTS/fn; EXPORTS.mkdir(exist_ok=True)
                filepath.write_text(code, encoding="utf-8")
                validation = self._validate_rust(filepath)
                result = f"Saved: {fn} | Validated: {validation}\n\n{result}"

            elif cmd in ("/explain",) and query:
                result = self.ask_llm(f"Explain this Rust concept with code examples: {query}")

            elif cmd=="/cargopath" and query:
                new_path = Path(query).expanduser().resolve()
                if new_path.exists(): self.cargo_path = str(new_path); result = f"Cargo path set to: {self.cargo_path}"
                else: result = f"Path not found: {new_path}"

            elif cmd in ("/cargo",) and query:
                allowed = {"build","check","test","run","clean","doc","fmt","clippy","bench","update","version","help"}
                parts_cmd = query.split()
                if not parts_cmd or parts_cmd[0] not in allowed: result = f"Allowed: {sorted(allowed)}"
                else:
                    try:
                        cargo_result = subprocess.run(["cargo"]+parts_cmd, capture_output=True, text=True, timeout=60, cwd=self.cargo_path)
                        result = cargo_result.stdout or cargo_result.stderr or "Cargo completed"
                    except Exception as e: result = f"Cargo error: {e}"

            elif cmd in ("/audit",) and query:
                standalone = self._run_standalone("audit", query)
                result = f"[Standalone audit]\n{standalone}" if standalone else self.ask_llm(f"Security audit this Rust code. Check unsafe blocks, unwraps, input validation. Code:\n{query[:4000]}")

            elif cmd in ("/pinch",) and query:
                standalone = self._run_standalone("pinch", query)
                result = f"[Standalone pinch]\n{standalone}" if standalone else self.ask_llm(f"Analyze for unnecessary clones and allocations. Code:\n{query[:4000]}")

            elif cmd in ("/fix","/debug") and query:
                result = self.ask_llm(f"Debug and fix this Rust code: {query[:4000]}")

            elif cmd in ("/test",) and query:
                result = self.ask_llm(f"Write Rust unit tests with #[cfg(test)]: {query[:4000]}")

            elif cmd in ("/run",):
                try:
                    run_result = subprocess.run(["cargo","run"], capture_output=True, text=True, timeout=30, cwd=self.cargo_path)
                    result = run_result.stdout or run_result.stderr or "Program completed"
                except Exception as e: result = f"Run error: {e}"

            elif query: result = self.ask_llm(f"Rust expert. Question: {query}")
            else: result = "Type /help for commands"

            from data_io import write_shared
            write_shared("crustyclaw_latest", {"command":cmd,"query":query,"result":str(result)[:500]})

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query",""); result = self.ask_llm(f"Write clean Rust 2024 edition code. Task: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

_agent = CrustyClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
