"""Guarded Executor — The ONLY legal way to perform dangerous operations.

   CONSTITUTIONAL LAW: No agent may directly call subprocess, os.system,
   shutil.rmtree, Path.unlink(), or any destructive operation.
   
   All dangerous operations MUST route through this executor.
   Every call checks ExecutionPolicy and records to DecisionLedger.
   
   This is the lock on the vault.
"""
import subprocess
import shutil
import os
from pathlib import Path
from typing import Dict, Optional, List

from shared.execution_policy import ExecutionPolicy, ApprovalLevel
from shared.decision_ledger import get_ledger


class GuardedExecutor:
    """The ONLY legal way to perform dangerous operations.
    
    Usage:
        executor = GuardedExecutor(agent="claw_coder")
        result = executor.delete_file("/path/to/file")  # Blocked by policy
        result = executor.git_commit("fix bug")          # Requires approval
        result = executor.run_subprocess(["ls", "-la"])  # Restricted
    """

    def __init__(self, agent: str = "unknown"):
        self.agent = agent
        self.ledger = get_ledger()

    def _check_and_record(self, action: str, context: dict = None) -> bool:
        """Check policy and record the attempt. Returns True if allowed."""
        policy = ExecutionPolicy.check(action)
        self.ledger.record_action(self.agent, action, policy, context)
        
        if not policy["allowed"]:
            if policy["level"] == ApprovalLevel.REQUIRE_APPROVAL:
                return ExecutionPolicy.request_approval(action, str(context))
            return False
        return True

    # === FILE OPERATIONS ===
    
    def delete_file(self, path: str) -> Dict:
        """Delete a file. BLOCKED by default."""
        if not self._check_and_record("ALLOW_DELETE", {"path": path}):
            return {"success": False, "error": "DELETE blocked by execution policy"}
        try:
            Path(path).unlink()
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_directory(self, path: str) -> Dict:
        """Delete a directory. BLOCKED by default."""
        if not self._check_and_record("ALLOW_DELETE", {"path": path, "type": "directory"}):
            return {"success": False, "error": "DELETE blocked by execution policy"}
        try:
            shutil.rmtree(path)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # === GIT OPERATIONS ===
    
    def git_commit(self, message: str, files: List[str] = None) -> Dict:
        """Git commit. REQUIRES APPROVAL."""
        context = {"message": message, "files": files}
        if not self._check_and_record("ALLOW_GIT_COMMIT", context):
            return {"success": False, "error": "Git commit requires approval"}
        try:
            cmd = ["git", "commit", "-m", message]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def git_push(self, remote: str = "origin", branch: str = "main") -> Dict:
        """Git push. REQUIRES APPROVAL."""
        context = {"remote": remote, "branch": branch}
        if not self._check_and_record("ALLOW_GIT_PUSH", context):
            return {"success": False, "error": "Git push requires approval"}
        try:
            cmd = ["git", "push", remote, branch]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def git_force_push(self, remote: str = "origin", branch: str = "main") -> Dict:
        """Git force push. PERMANENTLY BLOCKED."""
        return {"success": False, "error": "Git force push is PERMANENTLY BLOCKED by constitutional policy"}

    # === SHELL / SUBPROCESS ===
    
    def run_subprocess(self, cmd: List[str], timeout: int = 60) -> Dict:
        """Run a subprocess. RESTRICTED."""
        if not self._check_and_record("ALLOW_SUBPROCESS", {"cmd": cmd}):
            return {"success": False, "error": "Subprocess execution restricted"}
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Timeout after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_shell(self, command: str) -> Dict:
        """Run a raw shell command. PERMANENTLY BLOCKED."""
        return {"success": False, "error": "Shell execution is PERMANENTLY BLOCKED by constitutional policy"}

    # === NETWORK ===
    
    def network_push(self, url: str, data: str) -> Dict:
        """Push data to external network. REQUIRES APPROVAL."""
        if not self._check_and_record("ALLOW_NETWORK_PUSH", {"url": url}):
            return {"success": False, "error": "Network push requires approval"}
        import requests
        try:
            r = requests.post(url, data=data, timeout=30)
            return {"success": r.status_code < 400, "status": r.status_code}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # === DATABASE ===
    
    def db_destructive(self, operation: str, db_path: str) -> Dict:
        """Destructive database operation. BLOCKED."""
        return {"success": False, "error": f"Destructive DB operation BLOCKED: {operation}"}

    def db_schema_change(self, sql: str, db_path: str) -> Dict:
        """Database schema change. REQUIRES APPROVAL."""
        if not self._check_and_record("ALLOW_DB_SCHEMA_CHANGE", {"sql": sql[:200], "db": db_path}):
            return {"success": False, "error": "DB schema change requires approval"}
        import sqlite3
        try:
            db = sqlite3.connect(db_path)
            db.execute(sql)
            db.commit()
            db.close()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


__all__ = ["GuardedExecutor"]