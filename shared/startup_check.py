# shared/startup_check.py - Architectural invariant enforcement
# Validates universal commands against shared/universal_commands.json schema.
# Fails fast if any agent has drifted from the canonical implementation.
import os, json, hashlib

SCHEMA_PATH = 'shared/universal_commands.json'
REFERENCE_AGENT = 'lawclaw'

def verify_universal_commands():
    """Verify all universal commands match the canonical schema."""
    if not os.path.exists(SCHEMA_PATH):
        print(f"[STARTUP] Schema not found: {SCHEMA_PATH}")
        return False
    
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    
    commands = schema.get('universal_commands', {})
    violations = []
    ref_dir = f'agents/{REFERENCE_AGENT}/commands'
    
    for cmd_name, cmd_def in commands.items():
        cmd_file = cmd_def['file']
        ref_path = os.path.join(ref_dir, cmd_file)
        
        # Validate reference exists
        if not os.path.exists(ref_path):
            violations.append(f"REFERENCE MISSING: {REFERENCE_AGENT}/{cmd_file}")
            continue
        
        with open(ref_path, 'rb') as f:
            ref_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Validate all agents have identical copies
        for agent in sorted(os.listdir('agents')):
            if agent == REFERENCE_AGENT:
                continue
            if agent in ('exports', 'langclaw_backup', '__pycache__'):
                continue
            if agent.startswith('_'):
                continue
            
            agent_dir = f'agents/{agent}/commands'
            if not os.path.isdir(agent_dir):
                continue
            
            cmd_path = os.path.join(agent_dir, cmd_file)
            if not os.path.exists(cmd_path):
                violations.append(f"MISSING: {agent}/{cmd_file}")
                continue
            
            with open(cmd_path, 'rb') as f:
                agent_hash = hashlib.sha256(f.read()).hexdigest()
            
            if agent_hash != ref_hash:
                violations.append(f"DRIFT: {agent}/{cmd_file} differs from {REFERENCE_AGENT} reference")
    
    if violations:
        print("[STARTUP] ARCHITECTURAL INVARIANT VIOLATIONS:")
        for v in violations:
            print(f"  - {v}")
        print(f"[STARTUP] Universal commands defined in: {SCHEMA_PATH}")
        print(f"[STARTUP] Reference agent: {REFERENCE_AGENT}")
        print("[STARTUP] Fix: Copy from agents/lawclaw/commands/ to all agents.")
        return False
    
    print(f"[STARTUP] Universal command integrity verified: {len(commands)} commands across all agents")
    return True

print('shared/startup_check.py loaded')
