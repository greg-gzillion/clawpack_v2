"""WebClaw A2A Message Handler - Universal Agent Router"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

def process_task(task: str, agent: str = None) -> str:
    """Process incoming A2A task - routes to appropriate agent's command"""
    if not task:
        return "No task provided"

    task = task.strip()
    
    try:
        # If agent specified, try to route to that agent's command system
        if agent and agent != "webclaw":
            return route_to_agent_command(agent, task)
        
        # Handle WebClaw's own commands
        if task.startswith('/'):
            cmd_parts = task.split(maxsplit=1)
            cmd = cmd_parts[0].lower()
            args = cmd_parts[1] if len(cmd_parts) > 1 else ""
            
            # WebClaw native commands
            webclaw_commands = {
                '/fetch': 'fetch',
                '/browse': 'browse',
                '/chronicle': 'chronicle',
                '/llm': 'llm',
                '/recall': 'recall',
                '/share': 'share',
                '/cache': 'cache_stats',
                '/stats': 'stats',
                '/help': 'help',
                '/quit': 'quit',
                '/system': 'system',
                '/list': 'list'
            }
            
            if cmd in webclaw_commands:
                module_name = webclaw_commands[cmd]
                try:
                    cmd_module = __import__(f'commands.{module_name}', fromlist=['run'])
                    return cmd_module.run(args) or f"Command {cmd} executed"
                except Exception as e:
                    return f"Error running WebClaw command {cmd}: {e}"
        
        # Default: search the index for any query
        from providers.webclaw_provider import WebclawProvider
        provider = WebclawProvider()
        results = provider.search(task)
        
        if results:
            output = [f"Found {len(results)} results for '{task}':\n"]
            for r in results[:10]:
                output.append(f"  • {r}")
            return "\n".join(output)
        return f"No results found for: {task}"
            
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"


def route_to_agent_command(agent: str, task: str) -> str:
    """Route task to a specific agent's command system"""
    
    # Map agent names to their command directories
    agent_command_dirs = {
        'lawclaw': 'lawclaw/commands',
        'dataclaw': 'dataclaw/commands',
        'docuclaw': 'docuclaw/commands',
        'flowclaw': 'flowclaw/commands',
        'mathematicaclaw': 'mathematicaclaw/commands',
        'mediclaw': 'mediclaw/commands',
        'plotclaw': 'plotclaw/commands',
        'designclaw': 'designclaw/commands',
        'draftclaw': 'draftclaw/commands',
        'dreamclaw': 'dreamclaw/commands',
        'drawclaw': 'drawclaw/commands',
        'fileclaw': 'fileclaw/commands',
        'interpretclaw': 'interpretclaw/commands',
        'langclaw': 'langclaw/commands',
        'liberateclaw': 'liberateclaw/commands',
        'llmclaw': 'llmclaw/commands',
        'txclaw': 'TXclaw/commands',
        'claw_coder': 'claw_coder/commands',
        'rustypycraw': 'rustypycraw/commands',
        'webclaw': 'webclaw/commands'
    }
    
    if agent not in agent_command_dirs:
        # Fallback: search WebClaw index
        from providers.webclaw_provider import WebclawProvider
        provider = WebclawProvider()
        results = provider.search(task)
        if results:
            return f"Found {len(results)} results:\n" + "\n".join([f"  • {r}" for r in results[:10]])
        return f"No results for: {task}"
    
    # Try to load and execute the agent's command
    try:
        agent_path = Path(__file__).parent.parent / agent / 'commands'
        sys.path.insert(0, str(agent_path.parent))
        
        # Extract command and args
        if task.startswith('/'):
            parts = task.split(maxsplit=1)
            cmd = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            
            # Load the command module
            cmd_file = agent_path / f"{cmd[1:]}.py"
            if cmd_file.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location(cmd[1:], cmd_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'run'):
                    return module.run(args) or f"Command {cmd} executed"
                return f"Command {cmd} has no run function"
            else:
                # Command not found - search WebClaw index instead
                from providers.webclaw_provider import WebclawProvider
                provider = WebclawProvider()
                results = provider.search(task)
                if results:
                    return f"Found {len(results)} results:\n" + "\n".join([f"  • {r}" for r in results[:10]])
                return f"Command {cmd} not found in {agent}"
        else:
            # No slash command - treat as search query
            from providers.webclaw_provider import WebclawProvider
            provider = WebclawProvider()
            results = provider.search(task)
            if results:
                return f"Found {len(results)} results:\n" + "\n".join([f"  • {r}" for r in results[:10]])
            return f"No results for: {task}"
            
    except Exception as e:
        import traceback
        return f"Error routing to {agent}: {str(e)}\n{traceback.format_exc()}"
