'''Shared Files — Imperial Ministry of Documents.

   All file operations route through here. No agent handles files directly.
   FileClaw is the A2A frontend. This is the sovereign file authority.

   Usage:
       from shared.files import convert_file, analyze_file, batch_process, find_files, list_formats
'''
from .formats import SUPPORTED_FORMATS, EXTENSION_MAP, detect_type, calculate_hash, get_metadata, list_formats
from .converter import convert_file
from .analyzer import analyze_file
from .batch import batch_process
from .finder import find_files

__all__ = [
    'convert_file', 'analyze_file', 'batch_process', 'find_files',
    'list_formats', 'get_metadata', 'detect_type', 'calculate_hash',
    'SUPPORTED_FORMATS', 'EXTENSION_MAP',
]
