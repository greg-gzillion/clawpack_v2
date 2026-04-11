"""Clinical Command Handlers"""

class ClinicalCommands:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_procedure(self, procedure):
        if procedure:
            print(f"\n🔪 Procedure: {procedure}")
            print(self.agent.procedures(procedure))
            self.agent.session['queries'].append(procedure)
        else:
            print("Usage: /procedure <name>")
    
    def handle_prognosis(self, condition):
        if condition:
            print(f"\n📈 Prognosis: {condition}")
            print(self.agent.prognosis(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /prognosis <condition>")
    
    def handle_referral(self, condition):
        if condition:
            print(f"\n🏥 Referral: {condition}")
            print(self.agent.referral(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /referral <condition>")
