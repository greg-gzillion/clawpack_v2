# shared/speech.py - Multilingual speech synthesis abstraction
# All agents call speak(). This module handles voice routing, fallback, and profiles.
# Replaces direct pyttsx3 calls in /read, /voice, /interpret, and /speak.

import json, os
from pathlib import Path

# --- Voice profiles ---
PROFILES_PATH = 'data/tts_profiles.json'

def _load_profiles():
    try:
        with open(PROFILES_PATH) as f:
            return json.load(f)
    except:
        return {}

def _save_profiles(profiles):
    os.makedirs('data', exist_ok=True)
    with open(PROFILES_PATH, 'w') as f:
        json.dump(profiles, f, indent=2)

# --- Local TTS (pyttsx3) ---
def _speak_local(text, lang='en', rate=160):
    """Use system-installed voices via pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Try to match language
        for voice in voices:
            voice_langs = [l.lower()[:2] for l in voice.languages]
            if lang in voice_langs or lang in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.setProperty('rate', rate)
        engine.say(text)
        engine.runAndWait()
        return f"[TTS] Spoken ({lang})"
    except ImportError:
        return "[TTS] pyttsx3 not installed"
    except Exception as e:
        return f"[TTS] Error: {str(e)[:100]}"

# --- Cloud TTS fallback (for non-English) ---
def _speak_cloud(text, lang='en'):
    """Use Sovereign Gateway for TTS when local voices unavailable."""
    # For now: use the LLM to generate phonetic output
    # In production: route to Azure/OpenAI TTS API
    return f"[TTS] Cloud voice for {lang} not configured. Install {lang} voice in Windows Settings."

# --- Main speak function ---
def speak(text, lang=None, rate=None):
    """Speak text in the given language. Auto-detects from locale if not specified."""
    if lang is None:
        try:
            from shared.locale import get_language
            lang = get_language()
        except:
            lang = 'en'
    
    profiles = _load_profiles()
    
    # Check for saved voice preference
    voice_pref = profiles.get('voices', {}).get(lang, {})
    if rate is None:
        rate = voice_pref.get('rate', 160)
    
    # Try local first
    result = _speak_local(text, lang, rate)
    
    # If local fails for non-English, try cloud
    if 'Error' in result and lang != 'en':
        result = _speak_cloud(text, lang)
    
    return result

# --- Voice management ---
def list_voices(lang=None):
    """List available TTS voices, optionally filtered by language."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        result = "Available TTS Voices:\n"
        for i, v in enumerate(voices):
            voice_langs = [str(l)[:2].lower() for l in v.languages]
            if lang and lang not in voice_langs:
                continue
            gender = 'F' if 'zira' in v.name.lower() or 'sabina' in v.name.lower() or 'female' in v.name.lower() else 'M'
            result += f"  [{i}] {v.name} ({gender}) - {v.languages}\n"
        return result if '[' in result else f"No voices found for language '{lang}'. Install from Windows Settings > Speech."
    except ImportError:
        return "[TTS] pyttsx3 not installed. Run: pip install pyttsx3"

def set_voice(lang, voice_index):
    """Set preferred voice for a language."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            profiles = _load_profiles()
            if 'voices' not in profiles:
                profiles['voices'] = {}
            profiles['voices'][lang] = {
                'index': voice_index,
                'name': voices[voice_index].name,
                'rate': 160
            }
            _save_profiles(profiles)
            return f"[TTS] Voice for {lang}: {voices[voice_index].name}"
        return f"[TTS] Invalid voice index: {voice_index}"
    except ImportError:
        return "[TTS] pyttsx3 not installed"

def set_rate(lang, rate):
    """Set speaking rate for a language (50-400 words/min)."""
    rate = max(50, min(400, int(rate)))
    profiles = _load_profiles()
    if 'voices' not in profiles:
        profiles['voices'] = {}
    if lang not in profiles['voices']:
        profiles['voices'][lang] = {}
    profiles['voices'][lang]['rate'] = rate
    _save_profiles(profiles)
    return f"[TTS] Rate for {lang}: {rate} wpm"

def stop():
    """Stop current speech."""
    try:
        import pyttsx3
        pyttsx3.init().stop()
        return "[TTS] Stopped"
    except:
        return "[TTS] Nothing to stop"

def get_current_voice_info():
    """Get info about currently configured voices."""
    profiles = _load_profiles()
    voices = profiles.get('voices', {})
    if not voices:
        return "No voice preferences saved. Default system voice used."
    result = "Voice Preferences:\n"
    for lang, pref in voices.items():
        result += f"  {lang}: {pref.get('name', 'unknown')} @ {pref.get('rate', 160)} wpm\n"
    return result

# --- File reading ---
def read_file(filepath, lang=None):
    """Read a text file aloud."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        if len(text) > 50000:
            text = text[:50000] + "... [truncated]"
        speak(text, lang)
        return f"[TTS] Reading: {filepath} ({len(text)} chars)"
    except FileNotFoundError:
        return f"[TTS] File not found: {filepath}"
    except Exception as e:
        return f"[TTS] Error: {str(e)[:100]}"

print('shared/speech.py created')
