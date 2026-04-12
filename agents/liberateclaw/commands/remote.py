"""Remote command - Liberate models on remote GPU servers"""

def show_remote_help() -> str:
    return """
╔══════════════════════════════════════════════════════════════════╗
║  🌐 REMOTE LIBERATION - SSH to GPU Servers                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  USAGE:                                                          ║
║    /remote-liberate --user <user> --host <ip> --model <name>    ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    /remote-liberate --user greg --host 10.0.0.5 --model \       ║
║        meta-llama/Llama-3.1-70B-Instruct                        ║
║                                                                  ║
║    /remote-liberate --user root --host gpu-server --method \    ║
║        surgical --model mistralai/Mistral-7B-Instruct           ║
║                                                                  ║
║  REQUIREMENTS:                                                   ║
║    • SSH access to remote server                                ║
║    • OBLITERATUS installed on remote                            ║
║    • Sufficient GPU memory                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

def remote_liberate(args: str) -> str:
    """Liberate a model on a remote server via SSH"""
    import subprocess
    import shlex

    # Parse arguments
    parts = shlex.split(args)
    user = None
    host = None
    model = None
    method = "advanced"

    for i, part in enumerate(parts):
        if part == "--user" and i + 1 < len(parts):
            user = parts[i + 1]
        elif part == "--host" and i + 1 < len(parts):
            host = parts[i + 1]
        elif part == "--model" and i + 1 < len(parts):
            model = parts[i + 1]
        elif part == "--method" and i + 1 < len(parts):
            method = parts[i + 1]

    if not user or not host or not model:
        return show_remote_help()

    # Validate inputs to prevent injection
    if not all(c.isalnum() or c in '-_.@' for c in user):
        return "❌ Invalid username format"
    if not all(c.isalnum() or c in '-_.:' for c in host):
        return "❌ Invalid host format"
    if not all(c.isalnum() or c in '-_./:' for c in model):
        return "❌ Invalid model name format"

    try:
        # SECURE: Use list arguments with shell=False
        remote_cmd = f"obliteratus obliterate {model} --method {method}"
        ssh_cmd = ["ssh", f"{user}@{host}", remote_cmd]
        
        print(f"🔗 Connecting to {user}@{host}...")
        result = subprocess.run(
            ssh_cmd,
            shell=False,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            return f"✅ Remote liberation complete on {host}\n\n{result.stdout[:1000]}"
        else:
            return f"❌ Remote liberation failed:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return "❌ Remote operation timed out. Large models may need more time."
    except Exception as e:
        return f"❌ SSH connection failed: {e}"
