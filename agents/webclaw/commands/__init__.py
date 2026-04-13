# Commands for webclaw - safe imports
from .stats import stats_command
from .list import list_command
from .browse import browse_command
from .llm import llm_command
from .help import help_command
from .quit import quit_command
from .chronicle import run as chronicle_run

# Try importing optional commands
try:
    from .fetch import fetch_command
except ImportError:
    fetch_command = lambda args=None: "Fetch command unavailable - missing dependencies"

try:
    from .share import share_command
except ImportError:
    share_command = lambda args=None: "Share command unavailable"

try:
    from .recall import recall_command
except ImportError:
    recall_command = lambda args=None: "Recall command unavailable"

__all__ = [
    'stats_command',
    'list_command', 
    
    'browse_command',
    'fetch_command',
    'llm_command',
    'help_command',
    'share_command',
    'recall_command',
    'quit_command',
    'chronicle_run'
]

