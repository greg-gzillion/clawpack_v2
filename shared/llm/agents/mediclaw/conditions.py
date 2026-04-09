"""Medical Conditions Database - Organized by category"""

CONDITIONS = {
    "cardiovascular": [
        "hypertension", "coronary_artery_disease", "heart_failure",
        "arrhythmia", "myocardial_infarction", "cardiomyopathy"
    ],
    "neurological": [
        "stroke", "epilepsy", "migraine", "multiple_sclerosis",
        "parkinsons", "alzheimers", "meningitis"
    ],
    "respiratory": [
        "asthma", "copd", "pneumonia", "tuberculosis",
        "covid19", "influenza", "bronchitis"
    ],
    "gastrointestinal": [
        "gerd", "ulcer", "crohns", "colitis",
        "hepatitis", "cirrhosis", "pancreatitis"
    ],
    "endocrine": [
        "diabetes_type1", "diabetes_type2", "hypothyroidism",
        "hyperthyroidism", "cushings", "addisons"
    ],
    "musculoskeletal": [
        "arthritis", "osteoporosis", "fracture",
        "sprain", "tendonitis", "fibromyalgia"
    ],
    "infectious": [
        "hiv", "hepatitis_b", "hepatitis_c",
        "sepsis", "cellulitis", "osteomyelitis"
    ],
    "psychiatric": [
        "depression", "anxiety", "bipolar",
        "schizophrenia", "ptsd", "ocd", "adhd"
    ],
    "dermatological": [
        "eczema", "psoriasis", "acne",
        "melanoma", "basal_cell", "squamous_cell"
    ],
    "renal": [
        "ckd", "kidney_stones", "uti",
        "glomerulonephritis", "pyelonephritis"
    ]
}

class ConditionsDB:
    @staticmethod
    def get_condition(category: str, condition: str):
        """Get condition information"""
        return CONDITIONS.get(category, {}).get(condition, {})
    
    @staticmethod
    def list_categories():
        return list(CONDITIONS.keys())
    
    @staticmethod
    def search(query: str):
        results = []
        for category, conditions in CONDITIONS.items():
            for condition in conditions:
                if query.lower() in condition.lower():
                    results.append((category, condition))
        return results
