"""Lifestyle Command Handlers"""

class LifestyleCommands:
    def __init__(self, agent):
        self.agent = agent
    
    def handle_prevention(self, condition):
        if condition:
            print(f"\n🛡️ Prevention: {condition}")
            print(self.agent.prevention(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /prevention <condition>")
    
    def handle_diet(self, condition):
        if condition:
            print(f"\n🥗 Diet: {condition}")
            print(self.agent.diet(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /diet <condition>")
    
    def handle_exercise(self, condition):
        if condition:
            print(f"\n🏃 Exercise: {condition}")
            print(self.agent.exercise(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /exercise <condition>")
    
    def handle_natural(self, condition):
        if condition:
            print(f"\n🌿 Natural: {condition}")
            print(self.agent.natural(condition))
            self.agent.session['queries'].append(condition)
        else:
            print("Usage: /natural <condition>")
