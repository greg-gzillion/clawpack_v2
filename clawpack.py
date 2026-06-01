import os, sys, subprocess, socket, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{CYAN}

                          CLAWPACK V2 - AI AGENT ECOSYSTEM                        

   21 AI Agents     LLM Powered     A2A Ready     Chronicle        
{RESET}
""")
    try:
        from shared.accessibility import is_voice_active as voice_on
        from shared.locale import get_language, needs_translation
        status = []
        if voice_on():
            status.append("VOICE ACTIVE")
        if needs_translation():
            status.append(f"LANG:{get_language().upper()}")
        status_line = " | ".join(status) if status else "Press 'v' for voice"
        try:
            from shared.accessibility import get_active
            for t in get_active():
                status.append(t)
            status_line = " | ".join(status) if status else status_line
        except:
            pass
        print(f"{BOLD}{RED}    {status_line}{RESET}")
    except:
        pass

def get_active_model_display():
    models_dir = Path("models")
    active_file = models_dir / "active_model.json"
    if active_file.exists():
        with open(active_file) as f:
            data = json.load(f)
            model = data.get('model', 'none')
            source = data.get('source', 'stock')
            return f"{model} ({source})"
    return "none"

def show_agents():
    active_model = get_active_model_display()
    print(f"{CYAN}Active Model: {GREEN}{active_model}{RESET}\n")
    agents = [
        (1, "lawclaw", "Law Research & Analysis"),
        (2, "flowclaw", "Flowcharts & Diagrams"),
        (3, "docuclaw", "Document Creation"),
        (4, "mathematicaclaw", "Math & Computation"),
        (5, "liberateclaw", "Model Liberation"),
        (6, "txclaw", "TX Blockchain"),
        (7, "interpretclaw", "Translation & Speech"),
        (8, "langclaw", "Language Learning"),
        (9, "claw_coder", "Code Generation (39 langs)"),
        (10, "dataclaw", "Data Processing"),
        (11, "webclaw", "Web Search & References"),
        (12, "fileclaw", "File Operations"),
        (13, "plotclaw", "Charts & Graphs"),
        (14, "mediclaw", "Medical Analysis"),
        (15, "dreamclaw", "AI Vision & Generation"),
        (16, "designclaw", "Graphic Design"),
        (17, "draftclaw", "Technical Drawings"),
        (18, "crustyclaw", "Rust AI Assistant"),
        (19, "rustypycraw", "Code Crawler"),
        (20, "drawclaw", "AI Drawing & Art"),
        (21, "llmclaw", "Model Manager"),
    ]
    print("\n                          AVAILABLE AGENTS\n")
    for num, name, desc in agents:
        print(f" {num:3}  {name:<18} {desc}")
    print("\n  m    Switch Model")
    print("  q    Quit\n")

def launch_agent(agent_name):
    import requests
    print(f"{GREEN}Connecting to {agent_name} via A2A...{RESET}\n")
    print(f"{CYAN}Type 'exit' to return to menu{RESET}\n")
    while True:
        try:
            task = ""
            # Poll event bus for voice commands
            try:
                from shared.event_bus import get_event, EventIntent
                event = get_event(timeout=0.1)
                if event:
                    if event.intent == EventIntent.RUN_COMMAND:
                        task = event.raw_text
                        print(f"\n[VOICE] {task}")
                    elif event.intent == EventIntent.SWITCH_AGENT:
                        print(f"\n[VOICE] Switching...")
                        return
                    elif event.intent == EventIntent.SYSTEM_QUIT:
                        return
            except Exception:
                pass
            if not task:
                task = input(f"{BOLD}{GREEN}{agent_name}> {RESET}").strip()
            if not task:
                continue
            if task.lower() in ("exit", "quit", "q"):
                break
            print(f"{YELLOW}Thinking...{RESET}", end="\r")
            r = requests.post(f"http://127.0.0.1:8766/v1/message/{agent_name}",
                            json={"task": task}, timeout=300)
            if r.status_code == 200:
                result = r.json().get("result", "No response")
                print(" " * 30, end="\r")
                print(result)
            else:
                print(f"{RED}A2A error: {r.status_code}{RESET}")
        except Exception as e:
            if "Connection" in str(e):
                print(f"{RED}A2A server not running. Start with: python a2a_server.py{RESET}")
                break
            print(f"{RED}Error: {e}{RESET}")

def launch_model_selector():
    clear()
    print(f"{CYAN} LLM Model Selection{RESET}\n")
    subprocess.run([sys.executable, "agents/llmclaw/llmclaw.py"])

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_running = sock.connect_ex(('127.0.0.1', 8766)) == 0
    sock.close()
    if not server_running:
        print(f"{YELLOW} A2A Server not running on port 8766{RESET}")
        print(f"{YELLOW}   Start with: python a2a_server.py{RESET}")
        input("\nPress Enter to continue anyway...")

    agents_map = {
        1: "lawclaw", 2: "flowclaw", 3: "docuclaw", 4: "mathematicaclaw",
        5: "liberateclaw", 6: "txclaw", 7: "interpretclaw", 8: "langclaw",
        9: "claw_coder", 10: "dataclaw", 11: "webclaw", 12: "fileclaw",
        13: "plotclaw", 14: "mediclaw", 15: "dreamclaw", 16: "designclaw",
        17: "draftclaw", 18: "crustyclaw", 19: "rustypycraw", 20: "drawclaw",
        21: "llmclaw"
    }

    voice_name_map = {
        'law': '1', 'medic': '14', 'flow': '2', 'code': '9', 'coder': '9',
        'plot': '13', 'data': '10', 'web': '11', 'file': '12', 'dream': '15',
        'draw': '20', 'draft': '17', 'design': '16', 'rust': '18',
        'translate': '7', 'language': '8', 'math': '4', 'liberate': '5',
        'model': '21', 'llm': '21', 'doc': '3', 'blockchain': '6', 'tx': '6'
    }

    while True:
        banner()
        show_agents()
        choice = ""
        # Poll event bus for voice switch commands
        try:
            from shared.event_bus import get_event, EventIntent, pending_events
            n = pending_events()
            if n > 0:
                print(f'[DEBUG] {n} events pending')
            event = get_event(timeout=0.1)
            if event:
                print(f'[DEBUG] Got event: {event.intent.value}')
            if event and event.intent == EventIntent.SWITCH_AGENT:
                name = event.payload.get('name', '').lower()
                choice = voice_name_map.get(name, '')
                if choice:
                    print(f"\n[VOICE] -> agent {choice}")
        except Exception:
            pass
        if not choice:
            choice = input(f"\n{BOLD}{YELLOW} Select agent (1-21), v=voice b=braille n=neuralink e=eye s=voice-select, 'm' for model, or 'q' to quit: {RESET}").strip()

        if choice.lower() == 'q':
            clear()
            print(f"{GREEN} Goodbye!{RESET}")
            break
        elif choice.lower() == 'v':
            try:
                from shared.accessibility import toggle_voice, is_voice_active
                if is_voice_active():
                    toggle_voice()
                    print("  Voice deactivated.")
                else:
                    toggle_voice('lawclaw')
                    print("="*60)
                    print("  VOICE ACTIVE - Speak now.")
                    print("  Say: law, medic, code, dream, or a command.")
                    print("="*60)
            except Exception as e:
                print(f"Voice unavailable: {e}")
            continue
        elif choice.lower() == 'b':
            try:
                from shared.accessibility import toggle_braille
                state = toggle_braille()
                print(f"Braille: {'ON' if state else 'OFF'}")
            except Exception as e:
                print(f"Braille unavailable: {e}")
            continue
        elif choice.lower() == 'm':
            launch_model_selector()
            continue
        elif choice.isdigit():
            num = int(choice)
            if num in agents_map:
                launch_agent(agents_map[num])
            else:
                print(f"{RED} Invalid choice{RESET}")
        else:
            print(f"{RED} Invalid choice{RESET}")

if __name__ == "__main__":
    main()
