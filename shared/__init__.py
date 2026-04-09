"""Clawpack V2 - Production Patterns from Claude Code"""

# Pattern 6: File-Based Memory
from .memory import ClawpackMemory, get_memory, MemoryType

# Pattern 9: Slot Reservation
from .llm.slot_reservation import SlotReservation, get_slot_reservation

# Pattern 4: Fork Agents
from .fork import ForkManager, ForkConfig, ForkResult, SharedPrefixCache

# Pattern 5: Context Compression
from .compactor import ContextCompactor, get_compactor, CompressionResult

# Pattern 8: Sticky Latches
from .latches import StickyLatch, PromptLatches, get_latches

# Pattern 7: Two-Phase Skill Loading
from .skills import SkillManager, SkillLoader, Skill, SkillFrontmatter

# Pattern 10: Hook Config Snapshot
from .hooks import HookManager, HookSnapshot, HookConfig, HookPoint

# Existing I/O
from .input_handler import InputHandler, find_file, open_file
from .output_handler import OutputHandler, show_popup, save_image
from .edit_tools import EditTools, crop, enhance, resize

__all__ = [
    # Memory
    'ClawpackMemory', 'get_memory', 'MemoryType',
    # Slot Reservation
    'SlotReservation', 'get_slot_reservation',
    # Fork Agents
    'ForkManager', 'ForkConfig', 'ForkResult', 'SharedPrefixCache',
    # Compression
    'ContextCompactor', 'get_compactor', 'CompressionResult',
    # Latches
    'StickyLatch', 'PromptLatches', 'get_latches',
    # Skills
    'SkillManager', 'SkillLoader', 'Skill', 'SkillFrontmatter',
    # Hooks
    'HookManager', 'HookSnapshot', 'HookConfig', 'HookPoint',
    # I/O
    'InputHandler', 'find_file', 'open_file',
    'OutputHandler', 'show_popup', 'save_image',
    'EditTools', 'crop', 'enhance', 'resize'
]
