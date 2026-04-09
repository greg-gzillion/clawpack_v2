"""Command handlers"""
import subprocess

def handle_speak(text: str) -> str:
    ps = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
    subprocess.run(['powershell', '-Command', ps], capture_output=True)
    return f"🔊 {text}"

def handle_llms(manager) -> str:
    providers = manager.list_providers()
    return "Working LLMs:\n  • " + "\n  • ".join(providers)
