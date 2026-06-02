#!/bin/bash
echo "============================================================"
echo "  CLAWPACK V2 - Quick Install (Mac/Linux)"
echo "============================================================"
echo ""

if command -v python3 &> /dev/null; then
    echo "[OK] Python found: "
elif command -v python &> /dev/null; then
    echo "[OK] Python found: Python 3.12.10"
else
    echo "[ERROR] Python not found. Install Python 3.10+"
    exit 1
fi

if command -v ollama &> /dev/null; then
    echo "[OK] Ollama found"
else
    echo "[WARN] Ollama not found. Download from https://ollama.com"
fi

echo "[INSTALL] Installing Python packages..."
pip install -r requirements.txt -q
echo "[OK] Dependencies installed"

if command -v ollama &> /dev/null; then
    echo "[MODEL] Pulling deepseek-r1:8b (about 5GB)..."
    echo "        Press Ctrl+C to skip."
    ollama pull deepseek-r1:8b
fi

echo ""
echo "============================================================"
echo "  READY."
echo "  Start server:  python a2a_server.py"
echo "  Launch menu:   python clawpack.py"
echo "============================================================"
