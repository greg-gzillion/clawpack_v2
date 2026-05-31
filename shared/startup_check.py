# shared/startup_check.py - Architectural invariant enforcement
# Runs at server startup. Fails fast if universal commands have drifted.
import os
import hashlib

UNIVERSAL_COMMANDS = ['voice.py', 'listen.py', 'translate.py', 'read.py', 'braille_cmd.py', 'language.py']

def verify_universal_commands():
    """Verify all universal command files are identical to lawclaw's reference."""
    reference_dir = 'agents/lawclaw/commands'
    violations = []
    
    for cmd in UNIVERSAL_COMMANDS:
        ref_path = os.path.join(reference_dir, cmd)
        if not os.path.exists(ref_path):
            violations.append(f"REFERENCE MISSING: {cmd}")
            continue
        
        with open(ref_path, 'rb') as f:
            ref_hash = hashlib.sha256(f.read()).hexdigest()
        
        for agent in sorted(os.listdir('agents')):
            if agent in ('lawclaw', 'exports', 'langclaw_backup', '__pycache__') or agent.startswith('_') or not os.path.isdir(f'agents/{agent}/commands'):
                continue
            cmd_path = f'agents/{agent}/commands/{cmd}'
            if not os.path.exists(cmd_path):
                violations.append(f"MISSING: {agent}/{cmd}")
                continue
            with open(cmd_path, 'rb') as f:
                agent_hash = hashlib.sha256(f.read()).hexdigest()
            if agent_hash != ref_hash:
                violations.append(f"DRIFT: {agent}/{cmd} differs from lawclaw reference")
    
    if violations:
        print("[STARTUP] ARCHITECTURAL INVARIANT VIOLATIONS:")
        for v in violations:
            print(f"  - {v}")
        print("[STARTUP] Universal commands must be identical across all agents.")
        print("[STARTUP] Fix: Copy from agents/lawclaw/commands/ to all agents.")
        return False
    return True

print('shared/startup_check.py created')
