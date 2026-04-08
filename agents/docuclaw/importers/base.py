"""Base importer class"""
from abc import ABC, abstractmethod

class BaseImporter(ABC):
    name = ""
    extensions = []
    
    @abstractmethod
    def import_file(self, file_path):
        pass
    
    @abstractmethod
    def extract_text(self, content):
        pass
