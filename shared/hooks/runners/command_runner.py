"""Command hook runner - shell commands"""
import subprocess
import asyncio
import shlex
from pathlib import Path
from typing import Dict, Optional
from ..hook_types import HookResult, HookContext, HookExitCode

class CommandRunner:
    """Execute hooks as shell commands"""
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
    
    async def run(self, command: str, context: HookContext, input_data: Optional[Dict] = None) -> HookResult:
        """Run a command hook"""
        try:
            # Prepare environment
            env = {
                **context.environment,
                "CLAW_SESSION_ID": context.session_id or "",
                "CLAW_TOOL_NAME": context.tool_name or "",
                "CLAW_EVENT": context.event.value,
            }
            
            # Add input as JSON via stdin
            stdin_data = None
            if input_data:
                import json
                stdin_data = json.dumps(input_data)
            
            # Run command
            process = await asyncio.create_subprocess_exec(
                *shlex.split(command),
                stdin=asyncio.subprocess.PIPE if stdin_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=context.working_dir or Path.cwd(),
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=stdin_data.encode() if stdin_data else None),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return HookResult(
                    allowed=False,
                    block=True,
                    reason=f"Hook timed out after {self.timeout}s",
                )
            
            stdout_str = stdout.decode().strip()
            stderr_str = stderr.decode().strip()
            
            # Check exit code
            if process.returncode == HookExitCode.BLOCKING_ERROR.value:
                return HookResult(
                    allowed=False,
                    block=True,
                    reason=stderr_str or "Hook blocked execution",
                    stderr=stderr_str,
                    stdout=stdout_str,
                )
            elif process.returncode == HookExitCode.NON_BLOCKING_WARNING.value:
                return HookResult(
                    allowed=True,
                    block=False,
                    reason=stderr_str,
                    additional_context=stdout_str,
                    stderr=stderr_str,
                )
            else:
                # Try to parse JSON output
                if stdout_str and stdout_str.startswith('{'):
                    try:
                        import json
                        data = json.loads(stdout_str)
                        return HookResult(
                            allowed=data.get("allowed", True),
                            block=data.get("block", False),
                            modified_input=data.get("modified_input"),
                            additional_context=data.get("additional_context"),
                            reason=data.get("reason"),
                        )
                    except:
                        pass
                
                return HookResult(
                    allowed=True,
                    additional_context=stdout_str if stdout_str else None,
                    stdout=stdout_str,
                )
                
        except Exception as e:
            return HookResult(
                allowed=False,
                block=True,
                reason=f"Hook execution error: {str(e)}",
            )
