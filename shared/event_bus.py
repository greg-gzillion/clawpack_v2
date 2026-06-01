# shared/event_bus.py ? Canonical Event Bus for Clawpack V2
# All system input normalizes through here. Keyboard, voice, API, hardware.
# Constitutional: no privileged input pathway. All events governed equally.

import queue
import enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone

class EventSource(str, enum.Enum):
    KEYBOARD = "keyboard"
    VOICE = "voice"
    API = "api"
    SYSTEM = "system"
    ACCESSIBILITY = "accessibility"

class EventIntent(str, enum.Enum):
    SWITCH_AGENT = "switch_agent"
    LAUNCH_AGENT = "launch_agent"
    RUN_COMMAND = "run_command"
    TOGGLE_VOICE = "toggle_voice"
    TOGGLE_BRAILLE = "toggle_braille"
    TOGGLE_NEURALINK = "toggle_neuralink"
    TOGGLE_EYE = "toggle_eye"
    SLEEP_VOICE = "sleep_voice"
    WAKE_VOICE = "wake_voice"
    MENU_NAVIGATE = "menu_navigate"
    SYSTEM_QUIT = "system_quit"
    AGENT_RETURN = "agent_return"
    TIMEOUT = "timeout"

@dataclass
class CommandEvent:
    source: EventSource
    intent: EventIntent
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw_text: str = ""
    agent: str = ""

_event_queue: queue.Queue = queue.Queue()

def push_event(source, intent, payload=None, raw_text="", agent=""):
    event = CommandEvent(
        source=EventSource(source) if isinstance(source, str) else source,
        intent=EventIntent(intent) if isinstance(intent, str) else intent,
        payload=payload or {},
        raw_text=raw_text,
        agent=agent,
    )
    _event_queue.put(event)
    return event

def get_event(timeout=0.1):
    try:
        return _event_queue.get(timeout=timeout)
    except queue.Empty:
        return None

def pending_events():
    return _event_queue.qsize()

print("shared/event_bus.py created")
