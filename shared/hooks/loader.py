"""Hook loader - Discovers hooks from multiple sources"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
from .types import HookPoint, HookConfig


class HookLoader:
    """Load hooks from configuration files and directories"""
    
    def __init__(self):
        self.hooks_dir = Path.home() / ".clawpack" / "hooks"
        self.project_hooks_dir = Path.cwd() / ".clawpack" / "hooks"
        self.config_file = Path.home() / ".clawpack" / "hooks.json"
    
    def load_all(self) -> List[HookConfig]:
        """Load hooks from all sources"""
        hooks = []
        
        # Load from JSON config (highest priority)
        hooks.extend(self._load_from_config())
        
        # Load from hooks directory
        hooks.extend(self._load_from_directory(self.hooks_dir))
        
        # Load from project hooks
        hooks.extend(self._load_from_directory(self.project_hooks_dir))
        
        # Sort by priority (lower runs first)
        hooks.sort(key=lambda h: h.priority)
        
        return hooks
    
    def _load_from_config(self) -> List[HookConfig]:
        """Load hooks from JSON configuration"""
        hooks = []
        
        if self.config_file.exists():
            try:
                config = json.loads(self.config_file.read_text())
                
                for hook_data in config.get('hooks', []):
                    hook = HookConfig(
                        name=hook_data.get('name', 'unnamed'),
                        hook_point=HookPoint(hook_data['hook_point']),
                        command=hook_data['command'],
                        matcher=hook_data.get('matcher'),
                        enabled=hook_data.get('enabled', True),
                        timeout_seconds=hook_data.get('timeout', 30),
                        once=hook_data.get('once', False),
                        priority=hook_data.get('priority', 100),
                        trusted=hook_data.get('trusted', False),
                        allow_network=hook_data.get('allow_network', False)
                    )
                    hooks.append(hook)
            except Exception as e:
                print(f"⚠️ Error loading hooks config: {e}")
        
        return hooks
    
    def _load_from_directory(self, directory: Path) -> List[HookConfig]:
        """Load hooks from directory structure"""
        hooks = []
        
        if not directory.exists():
            return hooks
        
        # Structure: hooks/PreToolUse/script.sh
        for hook_point_dir in directory.iterdir():
            if not hook_point_dir.is_dir():
                continue
            
            try:
                hook_point = HookPoint(hook_point_dir.name)
            except ValueError:
                continue
            
            for script_file in hook_point_dir.glob("*"):
                if script_file.is_file() and self._is_executable(script_file):
                    hook = HookConfig(
                        name=script_file.stem,
                        hook_point=hook_point,
                        command=str(script_file),
                        matcher=None,  # Can be set in companion .json file
                        enabled=True,
                        timeout_seconds=30,
                        once=False,
                        priority=100,
                        trusted=False
                    )
                    
                    # Check for companion config
                    config_file = script_file.with_suffix('.json')
                    if config_file.exists():
                        try:
                            config = json.loads(config_file.read_text())
                            hook.matcher = config.get('matcher')
                            hook.priority = config.get('priority', 100)
                            hook.timeout_seconds = config.get('timeout', 30)
                            hook.once = config.get('once', False)
                        except:
                            pass
                    
                    hooks.append(hook)
        
        return hooks
    
    def _is_executable(self, path: Path) -> bool:
        """Check if file is executable"""
        return os.access(path, os.X_OK) or path.suffix in ['.sh', '.py', '.js', '.rb']
    
    def create_example_hooks(self):
        """Create example hooks for users to customize"""
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
        # Create PreToolUse example
        pre_tool_dir = self.hooks_dir / "PreToolUse"
        pre_tool_dir.mkdir(exist_ok=True)
        
        example_hook = pre_tool_dir / "example_validator.sh"
        example_hook.write_text("""#!/bin/bash
# Example PreToolUse hook - validates tool arguments
# Exit codes: 0=allow, 2=block, 1=warn

TOOL_NAME="$1"
shift

case "$TOOL_NAME" in
    "send_transaction")
        # Check amount
        for arg in "$@"; do
            if [[ "$arg" =~ amount=([0-9]+) ]]; then
                amount="${BASH_REMATCH[1]}"
                if [ "$amount" -gt 1000 ]; then
                    echo "⚠️ Large transaction detected: $amount"
                    exit 1  # Warning only
                fi
            fi
        done
        ;;
    "rm"|"delete")
        echo "❌ Destructive command blocked by hook"
        exit 2  # Block
        ;;
esac

exit 0  # Allow
""")
        os.chmod(example_hook, 0o755)
        
        print(f"✅ Created example hook: {example_hook}")
