"""MedicLaw Base Module - Comprehensive Medical AI Agent"""

from .. import get_llm
from typing import Optional, Dict, Any
from pathlib import Path
import json

class MedicalSpecialty:
    """Base class for all medical specialties"""
    
    def __init__(self, name: str, llm=None):
        self.name = name
        self.llm = llm or get_llm()
    
    def diagnose(self, symptoms: str, patient_history: str = "") -> str:
        """Provide differential diagnosis"""
        prompt = f"As a {self.name} specialist, provide differential diagnosis for:\nSymptoms: {symptoms}\nHistory: {patient_history}"
        return self.llm.generate(prompt, task="medical").text
    
    def treatment(self, condition: str, severity: str = "moderate") -> str:
        """Recommend treatment options"""
        prompt = f"As a {self.name} specialist, recommend treatments for {condition} (severity: {severity})"
        return self.llm.generate(prompt, task="medical").text
    
    def refer(self, condition: str) -> str:
        """Determine if referral needed"""
        prompt = f"As a {self.name} specialist, should {condition} be referred to another specialist? Why?"
        return self.llm.generate(prompt, task="medical").text

class MedicLawCore:
    """Core MedicLaw orchestrator"""
    
    def __init__(self):
        self.llm = get_llm()
        self.specialties = {}
        self._load_specialties()
    
    def _load_specialties(self):
        """Load all medical specialties"""
        from .specialties import ALL_SPECIALTIES
        for specialty_name, specialty_class in ALL_SPECIALTIES.items():
            self.specialties[specialty_name] = specialty_class(self.llm)
    
    def get_specialty(self, name: str):
        """Get a specific medical specialty"""
        return self.specialties.get(name.lower())
    
    def list_specialties(self) -> list:
        """List all available specialties"""
        return list(self.specialties.keys())
    
    def diagnose(self, symptoms: str, specialty: str = "general") -> str:
        """Route to appropriate specialty for diagnosis"""
        if specialty in self.specialties:
            return self.specialties[specialty].diagnose(symptoms)
        
        # Auto-route based on symptoms
        routing_prompt = f"Based on these symptoms, which medical specialty is most appropriate? Symptoms: {symptoms}\nSpecialties: {', '.join(self.specialties.keys())}"
        suggested = self.llm.generate(routing_prompt, task="medical").text.lower()
        
        for spec in self.specialties:
            if spec in suggested:
                return self.specialties[spec].diagnose(symptoms)
        
        return "Unable to determine appropriate specialty. Please consult a primary care physician."
    
    def emergency(self, situation: str) -> str:
        """Handle emergency medical situations"""
        prompt = f"EMERGENCY: {situation}\nProvide immediate first aid instructions and when to call emergency services."
        return self.llm.generate(prompt, task="medical").text
