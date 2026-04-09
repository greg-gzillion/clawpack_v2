"""All Medical Specialties - 40+ Fields"""

from . import MedicalSpecialty

class Cardiology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Cardiology", llm)
    
    def analyze_ecg(self, ecg_data: str) -> str:
        prompt = f"Analyze this ECG finding: {ecg_data}"
        return self.llm.generate(prompt, task="medical").text

class Neurology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Neurology", llm)

class Oncology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Oncology", llm)

class Pediatrics(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Pediatrics", llm)

class Psychiatry(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Psychiatry", llm)

class Radiology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Radiology", llm)

class Surgery(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Surgery", llm)

class EmergencyMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Emergency Medicine", llm)

class Anesthesiology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Anesthesiology", llm)

class Dermatology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Dermatology", llm)

class Endocrinology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Endocrinology", llm)

class Gastroenterology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Gastroenterology", llm)

class Geriatrics(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Geriatrics", llm)

class Hematology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Hematology", llm)

class InfectiousDisease(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Infectious Disease", llm)

class Nephrology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Nephrology", llm)

class ObstetricsGynecology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Obstetrics & Gynecology", llm)

class Ophthalmology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Ophthalmology", llm)

class Orthopedics(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Orthopedics", llm)

class Otolaryngology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Otolaryngology (ENT)", llm)

class Pathology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Pathology", llm)

class PhysicalMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Physical Medicine & Rehabilitation", llm)

class PlasticSurgery(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Plastic Surgery", llm)

class Podiatry(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Podiatry", llm)

class Pulmonology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Pulmonology", llm)

class Rheumatology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Rheumatology", llm)

class Urology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Urology", llm)

class AllergyImmunology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Allergy & Immunology", llm)

class CriticalCare(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Critical Care Medicine", llm)

class Genetics(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Medical Genetics", llm)

class NuclearMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Nuclear Medicine", llm)

class PreventiveMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Preventive Medicine", llm)

class AddictionMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Addiction Medicine", llm)

class AdolescentMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Adolescent Medicine", llm)

class ClinicalPharmacology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Clinical Pharmacology", llm)

class ForensicPathology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Forensic Pathology", llm)

class HospicePalliative(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Hospice & Palliative Medicine", llm)

class MedicalToxicology(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Medical Toxicology", llm)

class SleepMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Sleep Medicine", llm)

class SportsMedicine(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Sports Medicine", llm)

class TransplantSurgery(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Transplant Surgery", llm)

class TraumaSurgery(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Trauma Surgery", llm)

class VascularSurgery(MedicalSpecialty):
    def __init__(self, llm):
        super().__init__("Vascular Surgery", llm)

# Registry of all specialties
ALL_SPECIALTIES = {
    "cardiology": Cardiology,
    "neurology": Neurology,
    "oncology": Oncology,
    "pediatrics": Pediatrics,
    "psychiatry": Psychiatry,
    "radiology": Radiology,
    "surgery": Surgery,
    "emergency_medicine": EmergencyMedicine,
    "anesthesiology": Anesthesiology,
    "dermatology": Dermatology,
    "endocrinology": Endocrinology,
    "gastroenterology": Gastroenterology,
    "geriatrics": Geriatrics,
    "hematology": Hematology,
    "infectious_disease": InfectiousDisease,
    "nephrology": Nephrology,
    "obgyn": ObstetricsGynecology,
    "ophthalmology": Ophthalmology,
    "orthopedics": Orthopedics,
    "ent": Otolaryngology,
    "pathology": Pathology,
    "physical_medicine": PhysicalMedicine,
    "plastic_surgery": PlasticSurgery,
    "podiatry": Podiatry,
    "pulmonology": Pulmonology,
    "rheumatology": Rheumatology,
    "urology": Urology,
    "allergy": AllergyImmunology,
    "critical_care": CriticalCare,
    "genetics": Genetics,
    "nuclear_medicine": NuclearMedicine,
    "preventive": PreventiveMedicine,
    "addiction": AddictionMedicine,
    "adolescent": AdolescentMedicine,
    "clinical_pharm": ClinicalPharmacology,
    "forensic": ForensicPathology,
    "hospice": HospicePalliative,
    "toxicology": MedicalToxicology,
    "sleep": SleepMedicine,
    "sports": SportsMedicine,
    "transplant": TransplantSurgery,
    "trauma": TraumaSurgery,
    "vascular": VascularSurgery
}
