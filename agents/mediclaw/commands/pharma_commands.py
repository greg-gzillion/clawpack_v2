"""Pharmacology Command Handlers"""

class PharmaCommands:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_medications(self, drug):
        if drug:
            print(f"\n💊 Medication: {drug}")
            print(self.agent.medications(drug))
            self.agent.session['queries'].append(drug)
        else:
            print("Usage: /medications <drug>")
    
    def handle_interactions(self, drugs):
        if drugs:
            print(f"\n⚠️ Interactions: {drugs}")
            print(self.agent.interactions(drugs))
            self.agent.session['queries'].append(drugs)
        else:
            print("Usage: /interactions <drug1,drug2>")
    
    def handle_warnings(self, drug):
        if drug:
            print(f"\n⚠️ Warnings: {drug}")
            print(self.agent.warnings(drug))
            self.agent.session['queries'].append(drug)
        else:
            print("Usage: /warnings <drug>")
