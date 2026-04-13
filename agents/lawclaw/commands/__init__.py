#!/usr/bin/env python3
"""
Command Registry for LawClaw
Works with commands that have 'name' variable and 'run' function
"""

import importlib
from pathlib import Path

COMMAND_REGISTRY = {}

def load_all_commands():
    """Load all command modules using the name/run pattern"""
    commands_dir = Path(__file__).parent
    
    print("Loading command modules...")
    loaded_count = 0
    
    for py_file in sorted(commands_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        
        module_name = py_file.stem
        
        try:
            module = importlib.import_module(f"commands.{module_name}")
            
            # Check if module has 'name' attribute and 'run' function
            if hasattr(module, 'name') and hasattr(module, 'run'):
                cmd_name = module.name
                COMMAND_REGISTRY[cmd_name] = module.run
                print(f"  ✅ Loaded: {cmd_name}")
                loaded_count += 1
            else:
                print(f"  ⚠️ Skipped {module_name}.py (missing 'name' or 'run')")
                
        except Exception as e:
            print(f"  ❌ Error loading {module_name}: {e}")
    
    print(f"\n✅ Total commands loaded: {loaded_count}")
    return COMMAND_REGISTRY

def get_command_help():
    """Generate help text from all registered commands"""
    commands = sorted(COMMAND_REGISTRY.keys())
    
    help_lines = []
    help_lines.append("╔══════════════════════════════════════════════════════════════════╗")
    help_lines.append("║                    ⚖️ LAWCLAW COMMANDS ⚖️                        ║")
    help_lines.append("╠══════════════════════════════════════════════════════════════════╣")
    
    # Group commands by category
    categories = {
        "COURT RESEARCH": ["/court", "/federal", "/state", "/browse", "/jurisdiction"],
        "LAW RESEARCH": ["/search", "/ask", "/cite", "/statute", "/precedent", "/law"],
        "CASE INFO": ["/docket", "/judge", "/brief", "/oral", "/analyze"],
        "DOCUMENTS": ["/summarize", "/list"],
        "SYSTEM": ["/stats", "/help", "/quit"]
    }
    
    for category, cmd_list in categories.items():
        help_lines.append(f"║ {category:<66}║")
        for cmd in cmd_list:
            if cmd in commands:
                help_lines.append(f"║   {cmd:<20}                              ║")
        help_lines.append("╠══════════════════════════════════════════════════════════════════╣")
    
    # Add any additional commands not in categories
    extra_cmds = [c for c in commands if c not in sum(categories.values(), []) and c not in ["/help", "/quit"]]
    if extra_cmds:
        help_lines.append("║ ADDITIONAL:                                                     ║")
        for cmd in extra_cmds:
            help_lines.append(f"║   {cmd:<20}                              ║")
        help_lines.append("╠══════════════════════════════════════════════════════════════════╣")
    
    help_lines.append("║ SYSTEM:                                                          ║")
    help_lines.append("║   /stats                   - Statistics                         ║")
    help_lines.append("║   /help                    - This help                          ║")
    help_lines.append("║   /quit                    - Exit                               ║")
    help_lines.append("╚══════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(help_lines)

# Load commands when imported
load_all_commands()
