"""Core Command Handlers"""

class CoreCommands:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_sources(self):
        sources = self.agent.list_sources()
        print(f"\n📚 Sources ({len(sources)}):")
        for i, s in enumerate(sources[:30], 1):
            print(f"   {i}. {s}")
    
    def handle_stats(self):
        print(f"\n📊 Started: {self.agent.session['started']}")
        print(f"   Queries: {len(self.agent.session['queries'])}")
        print(f"   Sources: {len(self.agent.list_sources())}")
    
    def handle_research(self, query):
        if query:
            print(f"\n🔬 Researching: {query}")
            print(self.agent.research(query))
            self.agent.session['queries'].append(query)
        else:
            print("Usage: /research <topic>")
    
    def handle_diagnose(self, symptoms):
        if symptoms:
            print(f"\n🩺 Diagnosing: {symptoms}")
            print(self.agent.diagnose(symptoms))
            self.agent.session['queries'].append(symptoms)
        else:
            print("Usage: /diagnose <symptoms>")
    
    def handle_treatment(self, condition):
        if condition:
            print(f"\n💊 Treatment: {condition}")
            print(self.agent.treatment(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /treatment <condition>")
