'''FileClaw Core — now delegates to shared/files/ (Imperial Ministry of Documents).'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.files import convert_file, analyze_file, batch_process, find_files, list_formats

class FileClawCore:
    '''ADAPTER — delegates all file operations to shared/files/.'''

    def __init__(self):
        self.supported_formats = list_formats()

    def analyze_file(self, file_path: str):
        return analyze_file(file_path, use_ai=True)

    def convert_file(self, input_path: str, target_format: str):
        return convert_file(input_path, target_format)

    def batch_process(self, directory: str, operation: str):
        return batch_process(directory, operation)

    def find_files(self, query: str, search_path: str = None):
        return find_files(query, search_path)
