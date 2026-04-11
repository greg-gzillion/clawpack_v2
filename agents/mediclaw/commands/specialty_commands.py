"""Specialty Command Handlers"""

class SpecialtyCommands:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_pediatrics(self, issue):
        if issue:
            print(f"\n👶 Pediatric: {issue}")
            print(self.agent.pediatrics(issue))
            self.agent.session['queries'].append(issue)
        else:
            print("Usage: /pediatrics <issue>")
    
    def handle_geriatrics(self, issue):
        if issue:
            print(f"\n👴 Geriatric: {issue}")
            print(self.agent.geriatrics(issue))
            self.agent.session['queries'].append(issue)
        else:
            print("Usage: /geriatrics <issue>")
    
    def handle_lab(self, test):
        if test:
            print(f"\n🔬 Lab: {test}")
            print(self.agent.lab_tests(test))
            self.agent.session['queries'].append(test)
        else:
            print("Usage: /lab <test>")
    
    def handle_icd(self, diagnosis):
        if diagnosis:
            print(f"\n📋 ICD-10: {diagnosis}")
            print(self.agent.coding(diagnosis))
            self.agent.session['queries'].append(diagnosis)
        else:
            print("Usage: /icd <diagnosis>")
