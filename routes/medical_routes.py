"""Mediclaw routing"""
class MedicalRoutes:
    commands = ['/med', '/medical', '/symptom', '/treatment', '/drug']
    agent = 'mediclaw'
    
    @staticmethod
    def get_help():
        return """
🏥 MEDICAL:
  /med <condition>          - Medical information
  /symptom <symptom>        - Symptom checker
  /drug <name>              - Drug information
"""
