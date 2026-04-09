"""Diagnostic Tools and Guidelines"""

DIAGNOSTIC_TOOLS = {
    "laboratory": ["cbc", "basic_metabolic", "liver_function", "lipid_panel", "a1c", "thyroid"],
    "imaging": ["xray", "ct", "mri", "ultrasound", "pet", "mammogram"],
    "cardiac": ["ecg", "echocardiogram", "stress_test", "holter_monitor"],
    "neurological": ["eeg", "nerve_conduction", "lumbar_puncture", "neurological_exam"],
    "pulmonary": ["pft", "chest_xray", "ct_chest", "bronchoscopy"],
    "endoscopic": ["endoscopy", "colonoscopy", "cystoscopy", "laparoscopy"]
}

class Diagnostics:
    @staticmethod
    def get_tool(category: str):
        return DIAGNOSTIC_TOOLS.get(category, [])
    
    @staticmethod
    def interpret_result(test: str, result: str, llm):
        prompt = f"Interpret this {test} result: {result}. Include normal ranges and clinical significance."
        return llm.generate(prompt, task="medical").text
