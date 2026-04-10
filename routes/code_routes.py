"""Claw_coder routing"""
class CodeRoutes:
    commands = ['code', 'coder', '/write', '/review', '/test']
    agent = 'claw_coder'
    
    @staticmethod
    def get_help():
        return """
💻 CODE:
  code <prompt>             - Generate code
  /review <file>            - Code review
  /test <function>          - Generate tests
"""
