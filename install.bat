@echo off
echo ============================================================
echo   CLAWPACK V2 - Quick Install (Windows)
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
echo [OK] Python found

:: Check Ollama
ollama --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Ollama not found. Download from https://ollama.com
    echo        Clawpack works best with local models via Ollama.
    echo        You can use cloud API keys instead (Groq, Anthropic, OpenRouter).
    echo.
)
echo [OK] Environment checked

:: Install Python dependencies
echo.
echo [INSTALL] Installing Python packages...
pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Package installation failed. Try: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies installed

:: Pull a model if Ollama is available
ollama --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [MODEL] Pulling deepseek-r1:8b (about 5GB, one time only)...
    echo         Press Ctrl+C to skip and use cloud APIs instead.
    ollama pull deepseek-r1:8b
)

echo.
echo ============================================================
echo   READY.
echo.
echo   Start the server:  python a2a_server.py
echo   Launch the menu:   python clawpack.py
echo.
echo   Then try: /court Denver CO
echo ============================================================
pause
