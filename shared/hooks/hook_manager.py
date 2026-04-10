"""Hook manager - register and execute hooks"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .hook_types import HookEvent, HookDefinition, HookResult, HookContext
from .hook_matcher import HookMatcher
from .runners import CommandRunner, PromptRunner, HttpRunner, AgentRunner


@dataclass
class RegisteredHook:
    """A registered hook instance"""
    definition: HookDefinition
    matcher: Optional[HookMatcher] = None
    executed: bool = False


class HookManager:
    """Central hook registry and execution"""
    
    def __init__(self, llm_manager=None):
        self._hooks: Dict[HookEvent, List[RegisteredHook]] = {}
        self._snapshot = None
        self.llm_manager = llm_manager
        self._runners = {
            "command": CommandRunner(),
            "prompt": PromptRunner(llm_manager),
            "http": HttpRunner(),
            "agent": AgentRunner(),
        }
        self._load_from_settings()
    
    def _load_from_settings(self):
        """Load hooks from settings.json"""
        settings_paths = [
            Path.home() / ".clawpack" / "settings.json",
            Path.cwd() / ".clawpack" / "settings.json",
        ]
        
        for path in settings_paths:
            if path.exists():
                try:
                    data = json.loads(path.read_text())
                    hooks_config = data.get("hooks", {})
                    self._load_hooks_from_config(hooks_config)
                except:
                    pass
    
    def _load_hooks_from_config(self, config: Dict):
        """Load hooks from config dictionary"""
        for event_name, hook_configs in config.items():
            try:
                event = HookEvent(event_name)
            except ValueError:
                continue
            
            if not isinstance(hook_configs, list):
                hook_configs = [hook_configs]
            
            for hook_cfg in hook_configs:
                definition = HookDefinition.from_dict(hook_cfg)
                matcher = None
                if hook_cfg.get("matcher"):
                    matcher = HookMatcher(hook_cfg["matcher"])
                
                self.register(event, definition, matcher)
    
    def register(self, event: HookEvent, definition: HookDefinition, matcher: HookMatcher = None):
        """Register a hook"""
        if event not in self._hooks:
            self._hooks[event] = []
        
        self._hooks[event].append(RegisteredHook(
            definition=definition,
            matcher=matcher,
            executed=False,
        ))
    
    def should_run(self, event: HookEvent, tool_name: str = None, tool_input: Dict = None) -> List[RegisteredHook]:
        """Check which hooks should run for this event/tool"""
        hooks_to_run = []
        
        for hook in self._hooks.get(event, []):
            # Check once-only
            if hook.definition.once and hook.executed:
                continue
            
            # Check matcher
            if hook.matcher:
                if tool_name and hook.matcher.matches(tool_name, tool_input or {}):
                    hooks_to_run.append(hook)
            else:
                hooks_to_run.append(hook)
        
        return hooks_to_run
    
    async def run(self, event: HookEvent, context: HookContext) -> HookResult:
        """Run all hooks for an event"""
        hooks_to_run = self.should_run(event, context.tool_name, context.tool_input)
        
        if not hooks_to_run:
            return HookResult(allowed=True)
        
        result = HookResult(allowed=True)
        
        for hook in hooks_to_run:
            runner = self._runners.get(hook.definition.type.value)
            if not runner:
                continue
            
            # Prepare input for hook
            hook_input = {
                "tool_name": context.tool_name,
                "tool_input": context.tool_input,
                "tool_use_id": context.tool_use_id,
                "message": context.message,
            }
            
            # Run hook
            hook_result = await runner.run(
                hook.definition.command or hook.definition.url or hook.definition.prompt,
                context,
                hook_input
            )
            
            hook.executed = True
            
            # Deny takes precedence
            if hook_result.block:
                return HookResult(
                    allowed=False,
                    block=True,
                    reason=hook_result.reason,
                    additional_context=hook_result.additional_context,
                )
            
            # Accumulate modifications
            if hook_result.modified_input:
                result.modified_input = hook_result.modified_input
                context.tool_input = hook_result.modified_input
            
            if hook_result.additional_context:
                result.additional_context = hook_result.additional_context
        
        return result
    
    def snapshot(self):
        """Freeze hook configuration (security)"""
        self._snapshot = {
            event: [h.definition for h in hooks]
            for event, hooks in self._hooks.items()
        }
        return self._snapshot
    
    def restore_snapshot(self):
        """Restore from frozen snapshot"""
        if self._snapshot is not None:
            self._hooks = {}
            for event, definitions in self._snapshot.items():
                for definition in definitions:
                    self.register(event, definition)
    
    def clear(self):
        """Clear all hooks"""
        self._hooks.clear()


# Global hook manager instance
_hook_manager: Optional[HookManager] = None

def get_hook_manager() -> HookManager:
    """Get global hook manager singleton"""
    global _hook_manager
    if _hook_manager is None:
        _hook_manager = HookManager()
    return _hook_manager
