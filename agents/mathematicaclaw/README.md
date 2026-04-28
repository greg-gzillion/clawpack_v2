# MathematicaClaw

Complete math engine with computational math, animated visualization, and AI-powered explanations.

## Setup

### Requirements
```bash
pip install sympy numpy matplotlib plotly
Verify Installation
bash
python -c "import sympy; import numpy; import matplotlib; import plotly; print('All dependencies ready')"
Quick Start
Start the A2A server and connect to mathematicaclaw from the menu.

Basic Commands
Command	Example	Description
/solve	/solve x**2 + 5*x + 6	Solve equations (polynomial, systems)
/derivative	/derivative x**3 * exp(x)	Compute derivatives
/integral	/integrate x**2 * sin(x)	Compute indefinite integrals
/limit	/limit sin(x)/x as x->0	Evaluate limits
/matrix	/matrix [[1,2],[3,4]]	Matrix operations (det, rref, eigenvalues)
/system	/system 2*x+y=7, x-3*y=-14	Solve linear systems
/simplify	/simplify (x**2-1)/(x-1)	Simplify expressions
/factor	/factor x**4-10*x**3+35*x**2-50*x+24	Factor polynomials
/expand	/expand (x+1)**3	Expand expressions
/plot	/plot sin(x) + cos(2*x)	Generate graph (opens in browser)
/animate	/animate sin(x+t) from t=0 to 4*pi	Interactive animation with time slider
/explain	/explain Riemann hypothesis proof	AI-powered mathematical explanation
Arithmetic
/add 2 3 4 | /subtract 10 3 | /multiply 2 3 4 | /divide 10 2 | /power 2 8 | /sqrt 144 | /percent 15 of 200

Syntax Guide
Variables: Use x, y, z, t. Always use ** for exponents: x**2 not x^2.

Functions: sin(x), cos(x), tan(x), exp(x), log(x), sqrt(x)

Constants: pi, E, oo (infinity)

Multiplication: Explicit only: 2*x not 2x. Implicit for parentheses: 2(x+1) OK.

Systems: Comma-separated equations: 2*x + y = 7, x - 3*y = -14

Matrices: Nested lists: [[1,2,3],[4,5,6],[7,8,10]]

Visualization
Static Plots
text
/plot sin(x)
/plot x**2 + 3*x - 2
/plot exp(-x**2) * cos(5*x)
Opens PNG in your browser. Files saved to exports/plot_*.png.

Animated Plots
text
/animate sin(x + t) from t=0 to 4*pi
/animate exp(-x**2) * cos(2*pi*t*x) from t=0 to 2
/animate 3d x**2 + y**2 + sin(t) from t=0 to 2*pi
Opens interactive HTML in browser with:

Play/Pause button

Time slider for manual scrubbing

Zoom and pan (3D: rotate, zoom, pan)

Hover tooltips

Files saved to exports/animate_*.html.

AI Explanations
Ask any math question for a detailed explanation with proofs and examples:

text
/explain derive the Euler-Lagrange equation
/explain explain Noether's theorem mathematically
/explain prove the central limit theorem
/explain explain the Atiyah-Singer index theorem
Uses Claude via LLMClaw. Requires A2A server running.

A2A Integration
MathematicaClaw inherits from BaseAgent and supports full A2A routing. Other agents can call:

python
self.call_agent("mathematicaclaw", "/solve x**2 - 4")
self.call_agent("mathematicaclaw", "/plot sin(x)")
File Structure
text
agents/mathematicaclaw/
├── agent_handler.py          # A2A handler with full command routing
├── commands/
│   ├── solve.py              # Equation solving
│   ├── algebra.py            # Simplify, factor, expand, evaluate
│   ├── calculus.py           # Derivative, integral, limit
│   ├── arithmetic.py         # Basic arithmetic operations
│   ├── math.py               # Advanced math functions
│   ├── system.py             # System utilities
│   ├── plot.py               # Static matplotlib plots
│   └── animate.py            # Interactive plotly animations
├── cli/                      # Command-line interface
├── visualization/            # Visualization utilities
├── core/                     # Core math engine
└── handlers/                 # Additional handlers
Troubleshooting
"could not parse" error: Check syntax — use ** for exponents, * for multiplication.

Plot opens but shows nothing: The function may have asymptotes or complex values in the plotted range. Try adjusting the range or the function.

Animation not loading: Ensure pip install plotly completed successfully.

No browser opens: Files are saved to exports/. Open them manually with any browser.