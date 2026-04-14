import os
import re
from pathlib import Path

def extract_functions_classes(filepath):
    """Extract function and class names from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)\s*[:(]', content)
        
        # Extract docstring
        docstring = ""
        doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if doc_match:
            docstring = doc_match.group(1).strip().split('\n')[0][:100]
        
        return {
            'functions': functions,
            'classes': classes,
            'docstring': docstring
        }
    except:
        return {'functions': [], 'classes': [], 'docstring': ''}

def scan_agent(agent_path):
    """Scan a single agent directory"""
    agent_name = agent_path.name
    result = [f"\n{'='*80}\n🤖 AGENT: {agent_name}\n{'='*80}"]
    result.append(f"Location: agents/{agent_name}/")
    
    # Main file
    main_file = agent_path / f"{agent_name}.py"
    if main_file.exists():
        info = extract_functions_classes(main_file)
        result.append(f"\n📄 {agent_name}.py - MAIN ENTRY ({main_file.stat().st_size} bytes)")
        if info['docstring']:
            result.append(f"   Purpose: {info['docstring']}")
        if info['functions']:
            result.append(f"   Functions: {', '.join(info['functions'])}")
        if info['classes']:
            result.append(f"   Classes: {', '.join(info['classes'])}")
    else:
        result.append(f"\n❌ {agent_name}.py - MISSING")
    
    # Commands directory
    commands_dir = agent_path / "commands"
    if commands_dir.exists():
        cmd_files = list(commands_dir.glob("*.py"))
        cmd_files = [f for f in cmd_files if f.name != "__init__.py"]
        result.append(f"\n📁 commands/ - {len(cmd_files)} commands")
        
        for cmd_file in sorted(cmd_files):
            info = extract_functions_classes(cmd_file)
            # Extract command name
            cmd_name = f"/{cmd_file.stem}"
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
                name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if name_match:
                    cmd_name = name_match.group(1)
            
            result.append(f"   📄 {cmd_file.name} - {cmd_name}")
            if info['docstring']:
                result.append(f"      {info['docstring'][:80]}")
            if info['functions']:
                result.append(f"      Functions: {', '.join(info['functions'])}")
        
        # Check __init__.py
        init_file = commands_dir / "__init__.py"
        if init_file.exists():
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'COMMAND_REGISTRY' in content:
                    result.append("   📄 __init__.py - Dynamic command registry")
    
    # Core directory
    core_dir = agent_path / "core"
    if core_dir.exists():
        core_files = list(core_dir.rglob("*.py"))
        core_files = [f for f in core_files if f.name != "__init__.py"]
        result.append(f"\n📁 core/ - {len(core_files)} modules")
        
        for core_file in sorted(core_files):
            info = extract_functions_classes(core_file)
            rel_path = str(core_file.relative_to(core_dir))
            result.append(f"   📄 {rel_path} ({core_file.stat().st_size} bytes)")
            if info['docstring']:
                result.append(f"      {info['docstring'][:80]}")
            if info['functions']:
                result.append(f"      Functions: {', '.join(info['functions'])}")
            if info['classes']:
                result.append(f"      Classes: {', '.join(info['classes'])}")
    
    # Providers directory
    providers_dir = agent_path / "providers"
    if providers_dir.exists():
        prov_files = list(providers_dir.glob("*.py"))
        prov_files = [f for f in prov_files if f.name != "__init__.py"]
        if prov_files:
            result.append(f"\n📁 providers/ - {len(prov_files)} providers")
            for prov_file in sorted(prov_files):
                info = extract_functions_classes(prov_file)
                result.append(f"   📄 {prov_file.name}")
                if info['docstring']:
                    result.append(f"      {info['docstring'][:80]}")
    
    # CLI directory
    cli_dir = agent_path / "cli"
    if cli_dir.exists():
        cli_files = list(cli_dir.rglob("*.py"))
        cli_files = [f for f in cli_files if f.name != "__init__.py"]
        if cli_files:
            result.append(f"\n📁 cli/ - {len(cli_files)} files")
            for cli_file in sorted(cli_files):
                rel_path = str(cli_file.relative_to(cli_dir))
                result.append(f"   📄 {rel_path}")
    
    # Other directories
    other_dirs = ["exports", "references", "cache", "docs", "utils", "modules", "engine", "handlers", "data", "output"]
    for dirname in other_dirs:
        dir_path = agent_path / dirname
        if dir_path.exists():
            files = list(dir_path.rglob("*"))
            files = [f for f in files if f.is_file()]
            if files:
                total_size = sum(f.stat().st_size for f in files)
                if total_size > 1024*1024:
                    size_str = f"{total_size/(1024*1024):.1f} MB"
                elif total_size > 1024:
                    size_str = f"{total_size/1024:.0f} KB"
                else:
                    size_str = f"{total_size} bytes"
                result.append(f"\n📁 {dirname}/ - {len(files)} files ({size_str})")
    
    return '\n'.join(result)

# Main execution
root = Path("C:/Users/greg/dev/clawpack_v2")
agents_dir = root / "agents"

# Get all agents
all_agents = [d for d in agents_dir.iterdir() if d.is_dir() and d.name not in ["shared", "fork", "backup", "__pycache__"]]

output = []
output.append("# CLAWPACK_V2 - COMPLETE AGENT DOCUMENTATION")
output.append("# Every Agent, Every File, Every Function\n")
output.append(f"AGENT COUNT: {len(all_agents)} TOTAL AGENTS\n")

for agent_dir in sorted(all_agents):
    print(f"Scanning {agent_dir.name}...")
    output.append(scan_agent(agent_dir))
    output.append("")

# Write to file
doc_path = root / "COMPLETE_AGENT_DOCUMENTATION.md"
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"\n✅ Documentation saved to: {doc_path}")
print(f"   Size: {doc_path.stat().st_size} bytes")
