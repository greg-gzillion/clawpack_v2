"""Commands package for WebClaw"""

# Import all command functions
from .stats import stats_command
from .list import list_command
from .search import search_command
from .browse import browse_command
from .fetch import fetch_command
from .llm import llm_command
from .share import share_command
from .recall import recall_command
from .help import help_command
from .system import system_command
from .cache_stats import cache_stats_command
from .quit import quit_command

__all__ = [
    'stats_command',
    'list_command',
    'search_command',
    'browse_command',
    'fetch_command',
    'llm_command',
    'share_command',
    'recall_command',
    'help_command',
    'system_command',
    'cache_stats_command',
    'quit_command'
]
