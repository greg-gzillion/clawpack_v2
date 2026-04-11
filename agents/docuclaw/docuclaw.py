#!/usr/bin/env python3
"""DocuClaw - Document Processor"""

import sys
from pathlib import Path

# Add the agent directory to path
AGENT_DIR = Path(__file__).parent
sys.path.insert(0, str(AGENT_DIR))

# Now imports work relative to agent directory
from modules.ai.assistant import AIAssistant
from modules.formatter.styles import Formatter
from modules.templates.docs import get_template, list_templates
from modules.media.handler import MediaHandler
from modules.export.handler import ExportHandler

# Rest of DocuClaw class...
