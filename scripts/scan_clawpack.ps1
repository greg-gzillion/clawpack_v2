cd C:\Users\greg\dev\clawpack_v2

@"
=== CLAWPACK_V2 FULL PROJECT ANALYSIS ===
Generated: $(Get-Date)

"@ | Out-File -FilePath clawpack_full_scan.txt -Encoding UTF8

# 1. Full directory tree (exclude venv, __pycache__, .git)
@"

========================================
1. FULL DIRECTORY TREE
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
tree /F /A . | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8

# 2. Key connection points - A2A server
@"

========================================
2. A2A SERVER
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "a2a_server*" -ErrorAction SilentlyContinue | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 3. Base agent
@"

========================================
3. BASE AGENT
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "base_agent*" -ErrorAction SilentlyContinue | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 4. Agent init files
@"

========================================
4. AGENT INIT FILES
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "__init__.py" -ErrorAction SilentlyContinue | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 5. Agent Python files (exclude venv)
@"

========================================
5. AGENT PYTHON FILES
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\venv\\" -and $_.FullName -notmatch "\\__pycache__\\" -and $_.FullName -notmatch "\\.git\\" } | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 6. Chronicle ledger
@"

========================================
6. CHRONICLE LEDGER
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Path "agents\webclaw\core" -Filter "*.py" -ErrorAction SilentlyContinue | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 7. Config files (exclude venv)
@"

========================================
7. CONFIG FILES
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Include "*.json","*.yaml","*.yml","*.toml","*.cfg" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\venv\\" } | ForEach-Object {
    "--- FILE: $($_.FullName) ---" | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
}

# 8. Connection pattern search
@"

========================================
8. CONNECTION PATTERNS
========================================

"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8

@"

--- A2A References ---
"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\venv\\" } | Select-String -Pattern "A2A|a2a_server|call_agent|agent_registry|agent_name" -AllMatches -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8

@"

--- Chronicle References ---
"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\venv\\" } | Select-String -Pattern "chronicle|chronicle_ledger|search_chronicle|record_fetch|recover_by_context" -AllMatches -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8

@"

--- Inter-agent Communication ---
"@ | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8
Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "\\venv\\" } | Select-String -Pattern "_gather_all_context|ask_memory|smart_ask|shared_context|agent_context" -AllMatches -ErrorAction SilentlyContinue | Out-File -FilePath clawpack_full_scan.txt -Append -Encoding UTF8

Write-Host "Scan complete: clawpack_full_scan.txt"
Write-Host "File size: $((Get-Item clawpack_full_scan.txt).Length) bytes"