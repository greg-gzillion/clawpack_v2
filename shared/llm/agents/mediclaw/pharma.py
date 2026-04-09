"""Pharmacology Database - Medications and interactions"""

MEDICATIONS = {
    "analgesics": ["acetaminophen", "ibuprofen", "naproxen", "aspirin"],
    "antibiotics": ["amoxicillin", "azithromycin", "ciprofloxacin", "doxycycline"],
    "antihypertensives": ["lisinopril", "amlodipine", "losartan", "metoprolol"],
    "antidiabetics": ["metformin", "insulin", "glipizide", "sitagliptin"],
    "antidepressants": ["sertraline", "fluoxetine", "escitalopram", "bupropion"],
    "antipsychotics": ["risperidone", "olanzapine", "quetiapine", "aripiprazole"],
    "anticoagulants": ["warfarin", "apixaban", "rivaroxaban", "heparin"],
    "statins": ["atorvastatin", "simvastatin", "rosuvastatin", "pravastatin"],
    "bronchodilators": ["albuterol", "salmeterol", "formoterol", "tiotropium"],
    "steroids": ["prednisone", "dexamethasone", "hydrocortisone", "methylprednisolone"]
}

class Pharmacology:
    @staticmethod
    def get_medication(name: str):
        for category, meds in MEDICATIONS.items():
            if name.lower() in [m.lower() for m in meds]:
                return {"category": category, "name": name}
        return None
    
    @staticmethod
    def check_interaction(drug1: str, drug2: str, llm):
        prompt = f"Check interaction between {drug1} and {drug2}. Include severity and recommendations."
        return llm.generate(prompt, task="medical").text
