# POWERSHELL_SURVIVAL_GUIDE.md
## Why This File Exists
On May 30, 2026, hours were lost to PowerShell-specific failures
when trying to write files, execute Python, and restart the A2A server.
This document exists so no future session repeats those failures.

## What FAILED (Do Not Repeat)

### 1. python -c with multi-line code
FAILED EVERY TIME. PowerShell mangles nested quotes, eats backslashes,
and randomly terminates strings mid-execution.

### 2. PowerShell heredocs containing Python code
FAILED EVERY TIME. Single-quoted heredocs terminate early when
they encounter Python single quotes. Double-quoted heredocs
expand PowerShell variables and break Python syntax.
The CLI locks up and requires Ctrl+C to recover.

### 3. Out-File for files over ~100 lines
FAILED SILENTLY. The file appears to write but is silently truncated.
Only discovered by checking GitHub or counting lines after the fact.

### 4. echo appending for multi-line content
FAILED. Cannot handle special characters, newlines in strings, or any
content more complex than a single plaintext sentence.

## What WORKED (Use These Patterns)

### Pattern 0: echo for small files (THE WINNER on May 30)
Deployed 60 command files to 21 agents with zero errors.
`powershell
echo "line" > file.py
echo "line2" >> file.py
`
Deploy: Get-ChildItem -Directory "agents" | ForEach-Object { Copy-Item source dest }
Contrast: batch Python injection corrupted ALL 21 handlers. Required git revert.

## What WORKED (Use These Patterns)

### Pattern A: Write a Python script to disk, then execute it
This is the ONLY method that reliably wrote files over 50 lines.
Keep the script under 50 lines to avoid Out-File truncation.

### Pattern B: For large files, construct content in Python programmatically
Have Python build the content as a list of lines, then join and write.
This avoids embedding file content in the PowerShell script entirely.

### Pattern C: Verify every file write immediately
python -c "print(len(open('target.md').read().splitlines()))"

### Pattern D: Read a file before modifying it
Get-Content "path/to/file.py" | Select-Object -First 5

## Server Management Commands
- Kill all Python: taskkill /F /IM python.exe 2>$null
- Clear bytecode cache (REQUIRED after shared/ module changes):
  Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
  Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
- Start server: python a2a_server.py (from C:\Users\greg\dev\clawpack_v2)
- Test server: python -c "import requests; r=requests.post('http://127.0.0.1:8766/v1/message/lawclaw',json={'task':'/stats'},timeout=10); print(r.status_code)"

## CRITICAL: Command Files vs Handler Injection
On May 30, batch Python injection corrupted ALL 21 agents. Required git revert to 03cd28c89.
Lesson: Write command files once, Copy-Item to deploy. Never inject into handlers.

## Why Python Files Are the Only Reliable Method
PowerShell and Python have conflicting string delimiters.
The ONLY safe boundary is a .py file on disk. Write it. Execute it. Delete it.
Never try to inline Python in PowerShell. It will fail.