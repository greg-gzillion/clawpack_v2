"""Command handlers for Mediclaw - Enhanced"""

class CommandHandler:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_sources(self):
        sources = self.agent.list_sources()
        print(f"\n📚 Medical Sources ({len(sources)}):")
        for i, s in enumerate(sources, 1):
            print(f"   {i:2}. {s}")
        if len(sources) > 30:
            print(f"   ... and {len(sources)-30} more")
    
    def handle_stats(self):
        stats = self.agent.get_stats()
        print(f"\n📊 Session Statistics:")
        print(f"   Started: {stats['started']}")
        print(f"   Queries: {stats['queries']}")
        print(f"   Sources: {stats['sources']}")
    
    def handle_research(self, query):
        if query:
            print(f"\n🔬 Researching: {query}")
            result = self.agent.research(query)
            print(f"\n{result}")
            self.agent.session['queries'].append(query)
        else:
            print("Usage: /research <topic>")
    
    def handle_diagnose(self, symptoms):
        if symptoms:
            print(f"\n🩺 Diagnosing: {symptoms}")
            result = self.agent.diagnose(symptoms)
            print(f"\n{result}")
            self.agent.session['queries'].append(symptoms)
        else:
            print("Usage: /diagnose <symptoms>")
    
    def handle_treatment(self, condition):
        if condition:
            print(f"\n💊 Treatment for: {condition}")
            result = self.agent.treatment(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /treatment <condition>")
    
    # NEW COMMANDS
    
    def handle_medications(self, drug):
        """Get medication information"""
        if drug:
            print(f"\n💊 Medication info: {drug}")
            result = self.agent.medications(drug)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"medication:{drug}")
        else:
            print("Usage: /medications <drug_name>")
    
    def handle_interactions(self, drugs):
        """Check drug interactions"""
        if drugs:
            print(f"\n⚠️ Checking interactions: {drugs}")
            result = self.agent.interactions(drugs)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"interactions:{drugs}")
        else:
            print("Usage: /interactions <drug1,drug2,drug3>")
    
    def handle_emergency(self, symptom):
        """Emergency triage"""
        if symptom:
            print(f"\n🚨 EMERGENCY TRIAGE: {symptom}")
            result = self.agent.emergency(symptom)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"emergency:{symptom}")
        else:
            print("Usage: /emergency <symptom>")
    
    def handle_procedures(self, procedure):
        """Medical procedure information"""
        if procedure:
            print(f"\n🔪 Procedure: {procedure}")
            result = self.agent.procedures(procedure)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"procedure:{procedure}")
        else:
            print("Usage: /procedure <procedure_name>")
    
    def handle_prevention(self, condition):
        """Prevention guidelines"""
        if condition:
            print(f"\n🛡️ Prevention: {condition}")
            result = self.agent.prevention(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"prevention:{condition}")
        else:
            print("Usage: /prevention <condition>")
    
    def handle_pediatrics(self, symptom):
        """Pediatric-specific information"""
        if symptom:
            print(f"\n👶 Pediatric: {symptom}")
            result = self.agent.pediatrics(symptom)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"pediatrics:{symptom}")
        else:
            print("Usage: /pediatrics <symptom_or_condition>")
    
    def handle_geriatrics(self, condition):
        """Geriatric-specific information"""
        if condition:
            print(f"\n👴 Geriatric: {condition}")
            result = self.agent.geriatrics(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"geriatrics:{condition}")
        else:
            print("Usage: /geriatrics <condition>")
    
    def handle_lab_tests(self, test):
        """Lab test interpretation"""
        if test:
            print(f"\n🔬 Lab Test: {test}")
            result = self.agent.lab_tests(test)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"lab:{test}")
        else:
            print("Usage: /lab <test_name>")
    
    def handle_diet(self, condition):
        """Dietary recommendations"""
        if condition:
            print(f"\n🥗 Diet for: {condition}")
            result = self.agent.diet(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"diet:{condition}")
        else:
            print("Usage: /diet <condition>")
    
    def handle_exercise(self, condition):
        """Exercise recommendations"""
        if condition:
            print(f"\n🏃 Exercise for: {condition}")
            result = self.agent.exercise(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"exercise:{condition}")
        else:
            print("Usage: /exercise <condition>")
    
    def handle_prognosis(self, condition):
        """Disease prognosis"""
        if condition:
            print(f"\n📈 Prognosis: {condition}")
            result = self.agent.prognosis(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"prognosis:{condition}")
        else:
            print("Usage: /prognosis <condition>")
    
    def handle_referral(self, condition):
        """Specialist referral"""
        if condition:
            print(f"\n🏥 Referral for: {condition}")
            result = self.agent.referral(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"referral:{condition}")
        else:
            print("Usage: /referral <condition>")
    
    def handle_natural_remedies(self, condition):
        """Natural/home remedies"""
        if condition:
            print(f"\n🌿 Natural remedies for: {condition}")
            result = self.agent.natural_remedies(condition)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"natural:{condition}")
        else:
            print("Usage: /natural <condition>")
    
    def handle_coding(self, diagnosis):
        """ICD-10 coding"""
        if diagnosis:
            print(f"\n📋 ICD-10 for: {diagnosis}")
            result = self.agent.coding(diagnosis)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"icd:{diagnosis}")
        else:
            print("Usage: /icd <diagnosis>")
    
    def handle_warnings(self, drug):
        """Drug warnings and contraindications"""
        if drug:
            print(f"\n⚠️ Warnings for: {drug}")
            result = self.agent.warnings(drug)
            print(f"\n{result}")
            self.agent.session['queries'].append(f"warning:{drug}")
        else:
            print("Usage: /warnings <drug_name>")
    
    def handle_clear(self):
        """Clear screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Screen cleared. Type /help for commands.")
