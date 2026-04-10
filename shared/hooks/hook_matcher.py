"""Hook matcher - matches tool calls against patterns"""
import re
from typing import Optional, Dict, Any

class HookMatcher:
    """Matches tool calls against pattern strings"""
    
    def __init__(self, pattern: str):
        self.pattern = pattern
        self._regex = self._compile(pattern)
    
    def _compile(self, pattern: str) -> re.Pattern:
        """Convert pattern to regex"""
        # Convert glob patterns to regex
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("*", ".*")
        regex_pattern = regex_pattern.replace("?", ".")
        
        # Handle tool-specific patterns: ToolName(args)
        if "(" in pattern and ")" in pattern:
            # Extract tool name and args pattern
            tool_match = re.match(r'^(\w+)\((.+)\)$', pattern)
            if tool_match:
                tool_name, args_pattern = tool_match.groups()
                regex_pattern = f"^{tool_name}\\(.*{args_pattern}.*\\)$"
        
        return re.compile(regex_pattern, re.IGNORECASE)
    
    def matches(self, tool_name: str, tool_input: Dict) -> bool:
        """Check if this matcher matches the tool call"""
        # Build the match string
        match_str = tool_name
        
        # Add command string if present (for Bash)
        if tool_name == "Bash" and "command" in tool_input:
            match_str = f"{tool_name}({tool_input['command']})"
        elif "file_path" in tool_input:
            match_str = f"{tool_name}({tool_input['file_path']})"
        
        return bool(self._regex.search(match_str))
