"""Mathematicaclaw routing"""
class MathRoutes:
    commands = ['add', 'solve', 'plot', 'derivative', 'integral', 
                'simplify', 'factor', 'expand', 'limit', 'power', 'sqrt']
    agent = 'mathematicaclaw'
    
    @staticmethod
    def get_help():
        return """
📐 MATH:
  add 2 3           - Add numbers
  plot x**2         - Plot function (opens window)
  solve x**2 = 16   - Solve equation
  derivative x**3   - Calculate derivative
  integral x**2     - Calculate integral
"""
