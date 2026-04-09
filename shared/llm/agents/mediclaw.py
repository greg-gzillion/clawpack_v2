"""Main MedicLaw Interface - Complete Medical AI System"""

from . import MedicLawCore
from .specialties import ALL_SPECIALTIES
from .conditions import ConditionsDB
from .pharma import Pharmacology
from .emergency import EmergencyProtocols
from .diagnostics import Diagnostics

class MedicLaw:
    """Complete medical AI assistant with 40+ specialties"""
    
    def __init__(self):
        self.core = MedicLawCore()
        self.conditions = ConditionsDB()
        self.pharma = Pharmacology()
        self.emergency = EmergencyProtocols()
        self.diagnostics = Diagnostics()
    
    def diagnose(self, symptoms: str, specialty: str = None) -> str:
        """Get diagnosis from appropriate specialty"""
        if specialty:
            return self.core.get_specialty(specialty).diagnose(symptoms)
        return self.core.diagnose(symptoms)
    
    def list_specialties(self) -> list:
        """List all available medical specialties"""
        return self.core.list_specialties()
    
    def emergency_guide(self, emergency_type: str) -> dict:
        """Get emergency protocol"""
        return self.emergency.get_protocol(emergency_type)
    
    def drug_interaction(self, drug1: str, drug2: str) -> str:
        """Check drug interactions"""
        return self.pharma.check_interaction(drug1, drug2, self.core.llm)
    
    def condition_info(self, condition: str) -> str:
        """Get information about a medical condition"""
        prompt = f"Provide comprehensive information about {condition}: symptoms, causes, diagnosis, treatment, prognosis."
        return self.core.llm.generate(prompt, task="medical").text
    
    def treatment_options(self, condition: str, specialty: str = None) -> str:
        """Get treatment options for a condition"""
        if specialty and specialty in self.core.specialties:
            return self.core.specialties[specialty].treatment(condition)
        
        prompt = f"What are the standard treatment options for {condition}? Include medications, procedures, and lifestyle changes."
        return self.core.llm.generate(prompt, task="medical").text
    
    def get_stats(self) -> dict:
        """Get system statistics"""
        return {
            "specialties": len(self.core.specialties),
            "conditions_categories": len(self.conditions.list_categories()),
            "medication_categories": len(MEDICATIONS),
            "emergency_protocols": len(self.emergency.list_emergencies()),
            "diagnostic_categories": len(DIAGNOSTIC_TOOLS)
        }
