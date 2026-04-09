"""Hook executor - Runs hooks and processes results"""

import asyncio
import subprocess
import json
import signal
from typing import List, Optional
from pathlib import Path

from .types import HookContext, HookResult, HookConfig, ExitCode, HookPoint


class HookExecutor:
    """Execute hooks with timeout and security controls"""
    
    def __init__(self, workspace_trusted: bool = False):
        self.workspace_trusted = workspace_trusted
        self._frozen_configs: List[HookConfig] = []
        self._frozen = False
    
    def freeze_configs(self, configs: List[HookConfig]):
        """Freeze hook configurations (snapshot security model)"""
        self._frozen_configs = configs.copy()
        self._frozen = True
    
    def get_matching_hooks(self, hook_point: HookPoint, context: HookContext) -> List[HookConfig]:
        """Get hooks that match the current context"""
        if not self._frozen:
            return []
        
        matching = []
        for config in self._frozen_configs:
            if not config.enabled:
                continue
            if config.hook_point != hook_point:
                continue
            if not config.matches(context):
                continue
            matching.append(config)
        
        return matching
    
    async def execute_hooks(
        self, 
        hook_point: HookPoint, 
        context: HookContext
    ) -> HookResult:
        """
        Execute all matching hooks.
        
        Returns the most restrictive result (BLOCK > WARNING > SUCCESS).
        Permission decisions: deny > ask > allow.
        """
        matching = self.get_matching_hooks(hook_point, context)
        
        if not matching:
            return HookResult(exit_code=ExitCode.SUCCESS)
        
        # Execute hooks in parallel (they're independent)
        tasks = [self._execute_one(hook, context) for hook in matching]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        final_result = HookResult(exit_code=ExitCode.SUCCESS)
        modified_input = None
        
        for result in results:
            if isinstance(result, Exception):
                print(f"⚠️ Hook error: {result}")
                continue
            
            if not isinstance(result, HookResult):
                continue
            
            # BLOCK overrides everything
            if result.should_block:
                return result
            
            # WARNING overrides SUCCESS
            if result.should_warn and final_result.exit_code == ExitCode.SUCCESS:
                final_result = result
            
            # Accumulate messages
            if result.message:
                if final_result.message:
                    final_result.message += "\n" + result.message
                else:
                    final_result.message = result.message
            
            # Keep the first modification
            if result.has_modifications and modified_input is None:
                modified_input = result.modified_input
                final_result.modified_input = modified_input
            
            # Permission precedence: deny > ask > allow
            if result.permission_decision:
                current = final_result.permission_decision
                if result.permission_decision == 'deny':
                    final_result.permission_decision = 'deny'
                elif result.permission_decision == 'ask' and current != 'deny':
                    final_result.permission_decision = 'ask'
                elif result.permission_decision == 'allow' and not current:
                    final_result.permission_decision = 'allow'
        
        # Auto-remove 'once' hooks that executed successfully
        for hook in matching:
            if hook.once:
                hook.enabled = False
        
        return final_result
    
    async def _execute_one(self, config: HookConfig, context: HookContext) -> HookResult:
        """Execute a single hook with timeout"""
        try:
            # Build command with context
            cmd = self._build_command(config.command, context)
            
            # Run with timeout
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send context as JSON to stdin
            context_json = json.dumps(context.to_dict())
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=context_json.encode()),
                timeout=config.timeout_seconds
            )
            
            # Parse result
            return self._parse_result(process.returncode, stdout, stderr)
            
        except asyncio.TimeoutError:
            return HookResult(
                exit_code=ExitCode.WARNING,
                message=f"Hook '{config.name}' timed out after {config.timeout_seconds}s"
            )
        except Exception as e:
            return HookResult(
                exit_code=ExitCode.WARNING,
                message=f"Hook '{config.name}' failed: {e}"
            )
    
    def _build_command(self, command: str, context: HookContext) -> List[str]:
        """Build shell command from config"""
        # Handle shebang scripts directly
        if command.startswith('#!'):
            return [command]
        
        # Handle scripts by extension
        if command.endswith('.py'):
            return ['python', command, context.tool_name or '', json.dumps(context.to_dict())]
        elif command.endswith('.js'):
            return ['node', command, context.tool_name or '', json.dumps(context.to_dict())]
        elif command.endswith('.rb'):
            return ['ruby', command, context.tool_name or '', json.dumps(context.to_dict())]
        elif command.endswith('.sh'):
            return ['bash', command, context.tool_name or '']
        
        # Default: run with shell
        return ['bash', '-c', command]
    
    def _parse_result(self, returncode: int, stdout: bytes, stderr: bytes) -> HookResult:
        """Parse hook output into HookResult"""
        stdout_str = stdout.decode('utf-8', errors='ignore').strip()
        stderr_str = stderr.decode('utf-8', errors='ignore').strip()
        
        message = stdout_str or stderr_str
        
        # Try to parse JSON output
        if stdout_str.startswith('{'):
            try:
                data = json.loads(stdout_str)
                return HookResult(
                    exit_code=ExitCode(data.get('exit_code', returncode)),
                    message=data.get('message', message),
                    modified_input=data.get('modified_input'),
                    permission_decision=data.get('permission'),
                    metadata=data.get('metadata', {})
                )
            except:
                pass
        
        # Fallback to exit code semantics
        if returncode == 0:
            exit_code = ExitCode.SUCCESS
        elif returncode == 2:
            exit_code = ExitCode.BLOCK
        else:
            exit_code = ExitCode.WARNING
        
        return HookResult(exit_code=exit_code, message=message)
