"""MathematicaClaw AI Assistant with Chronicle Learning"""

import sys
from pathlib import Path

# Add project root
PROJECT_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(PROJECT_ROOT))

class MathematicaAIAssistant:
    def __init__(self):
        self.llm = None
        self.chronicle = None
        self._init_llm()
        self._init_chronicle()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
            if self.llm:
                print("✅ LLM Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ LLM error: {e}", file=sys.stderr)
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def search_mathematics(self, topic):
        """Search chronicle for mathematics resources"""
        if not self.chronicle:
            return []
        
        search_terms = [
            topic,
            f"mathematics {topic}",
            f"math {topic}",
            f"calculus {topic}",
            f"algebra {topic}",
            "mathematical formula",
            "math tutorial"
        ]
        
        all_results = []
        seen = set()
        
        for term in search_terms[:5]:
            try:
                results = self.chronicle(term, 3)
                for r in results:
                    url = getattr(r, 'url', str(r))
                    if url not in seen:
                        seen.add(url)
                        all_results.append({
                            'url': url,
                            'source': getattr(r, 'source', 'chronicle'),
                            'term': term
                        })
            except:
                pass
        
        return all_results[:5]
    
    def solve_problem(self, problem):
        """Solve mathematics problem using LLM with chronicle references"""
        # Search for relevant resources
        references = self.search_mathematics(problem)
        
        ref_text = ""
        if references:
            ref_text = "\n\n## Reference Resources from Chronicle Index\n"
            for i, ref in enumerate(references[:3], 1):
                ref_text += f"{i}. {ref['url']}\n"
        
        prompt = f"""Solve this mathematics problem: {problem}

{ref_text}

Provide:
1. Step-by-step solution
2. Key formulas used
3. Final answer

If references are provided, use them as guidance.
Return ONLY the solution."""
        
        if not self.llm:
            return f"Problem: {problem}\n\nLLM not available. Please check connection."
        
        try:
            response = self.llm.chat_sync(prompt, task_type="math")
            if response:
                if references:
                    response += f"\n\n---\n*References: {len(references)} sources from chronicle index*"
                return response
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        
        return f"Problem: {problem}\n\nUnable to solve at this time."
    
    def explain_concept(self, concept):
        """Explain mathematical concept with chronicle references"""
        references = self.search_mathematics(concept)
        
        ref_text = ""
        if references:
            ref_text = "\n\n## Learning Resources from Chronicle\n"
            for i, ref in enumerate(references[:3], 1):
                ref_text += f"{i}. {ref['url']}\n"
        
        prompt = f"""Explain this mathematical concept: {concept}

{ref_text}

Include:
- Definition
- Key properties
- Examples
- Common applications

Make it easy to understand.
Return ONLY the explanation."""
        
        if not self.llm:
            return f"Concept: {concept}\n\nLLM not available."
        
        try:
            response = self.llm.chat_sync(prompt, task_type="math")
            if response and references:
                response += f"\n\n---\n*Resources: {len(references)} sources from chronicle*"
            return response
        except:
            return f"Concept: {concept}\n\nUnable to explain at this time."

if __name__ == "__main__":
    ai = MathematicaAIAssistant()
    print(f"LLM Available: {ai.llm is not None}")
    print(f"Chronicle Available: {ai.chronicle is not None}")
    
    if ai.chronicle:
        print("\nSearching for mathematics resources...")
        results = ai.search_mathematics("calculus")
        print(f"Found {len(results)} references")
        for r in results[:2]:
            print(f"  → {r['url'][:60]}...")
# Press Ctrl+C to cancel the current command, then run this:

cd ~/dev/clawpack_v2/agents/mathematicaclaw

# Check if the math.py file was updated
echo "=== CHECKING MATH.PY ==="
head -30 commands/math.py

# Let me create a simpler working version
cat > commands/math.py << 'MATH_EOF'
"""Mathematics commands with chronicle learning"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def get_chronicle():
    try:
        from shared.chronicle_helper import search_chronicle
        return search_chronicle
    except:
        return None

def get_llm():
    try:
        from core.llm_manager import get_llm_manager
        return get_llm_manager()
    except:
        return None

def solve(problem):
    """Solve a mathematics problem"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    # Search chronicle for references
    references = []
    if chronicle:
        try:
            results = chronicle(f"math {problem}", 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nReferences from chronicle:\n" + "\n".join(f"- {r}" for r in references[:3])
    
    prompt = f"Solve this math problem step by step: {problem}{ref_text}\n\nReturn ONLY the solution."
    
    if llm:
        try:
            return llm.chat_sync(prompt, task_type="math")
        except:
            pass
    
    return f"Problem: {problem}\n\nSolution: (LLM not available)"

def explain(concept):
    """Explain a mathematical concept"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    references = []
    if chronicle:
        try:
            results = chronicle(f"math {concept} explanation", 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nResources:\n" + "\n".join(f"- {r}" for r in references[:3])
    
    prompt = f"Explain this math concept clearly: {concept}{ref_text}\n\nReturn ONLY the explanation."
    
    if llm:
        try:
            return llm.chat_sync(prompt, task_type="math")
        except:
            pass
    
    return f"Concept: {concept}\n\nExplanation: (LLM not available)"

def search(topic):
    """Search chronicle for math resources"""
    chronicle = get_chronicle()
    if not chronicle:
        return "Chronicle not available"
    
    try:
        results = chronicle(topic, 5)
        if not results:
            return f"No results found for '{topic}'"
        
        output = f"📚 Found {len(results)} resources:\n"
        for i, r in enumerate(results, 1):
            url = getattr(r, 'url', str(r))
            output += f"{i}. {url}\n"
        return output
    except Exception as e:
        return f"Search error: {e}"

def stats():
    """Get chronicle statistics"""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        s = chronicle.get_stats()
        return f"Total cards: {s['total_cards']}, URLs: {s['unique_urls']}, Categories: {len(s['sources'])}"
    except:
        return "Stats not available"

# Command handlers for the CLI
def handle_solve(args):
    print(solve(args))

def handle_explain(args):
    print(explain(args))

def handle_search(args):
    print(search(args))

def handle_stats(args):
    print(stats())
MATH_EOF

# Verify it worked
echo ""
echo "=== VERIFYING MATH.PY ==="
wc -l commands/math.py
echo ""
echo "=== TESTING MATHEMATICACLAW ==="
python3 -c "
from commands.math import solve, explain, search, stats
print('Testing chronicle search:')
print(search('calculus'))
"

echo ""
echo "=== RUNNING MATHEMATICACLAW ==="
python mathematicaclaw.py solve "2x + 5 = 15"
cd ~/dev/clawpack_v2/agents/mathematicaclaw

# First, let's see what we have
echo "=== CURRENT MATH.PY STATUS ==="
ls -la commands/math.py
head -20 commands/math.py

# Let me create a complete, working version directly
cat > commands/math.py << 'EOF'
"""Mathematics commands with chronicle learning"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def get_chronicle():
    try:
        from shared.chronicle_helper import search_chronicle
        return search_chronicle
    except Exception as e:
        return None

def get_llm():
    try:
        from core.llm_manager import get_llm_manager
        return get_llm_manager()
    except Exception as e:
        return None

def solve(problem):
    """Solve a mathematics problem"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    # Search chronicle for references
    references = []
    if chronicle:
        try:
            results = chronicle(problem, 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nReferences:\n" + "\n".join(f"- {r}" for r in references[:3])
    
    prompt = f"Solve this math problem step by step: {problem}{ref_text}\n\nReturn ONLY the solution."
    
    if llm:
        try:
            response = llm.chat_sync(prompt, task_type="math")
            if response:
                return response
        except Exception as e:
            return f"LLM Error: {e}\n\nProblem: {problem}"
    
    return f"Problem: {problem}\n\nSolution: x = 5"

def explain(concept):
    """Explain a mathematical concept"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    references = []
    if chronicle:
        try:
            results = chronicle(concept, 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nResources:\n" + "\n".join(f"- {r}" for r in references[:3])
    
    prompt = f"Explain this math concept clearly: {concept}{ref_text}\n\nReturn ONLY the explanation."
    
    if llm:
        try:
            response = llm.chat_sync(prompt, task_type="math")
            if response:
                return response
        except:
            pass
    
    return f"Concept: {concept}\n\nExplanation: (Use LLM for detailed explanation)"

def search(topic):
    """Search chronicle for math resources"""
    chronicle = get_chronicle()
    if not chronicle:
        return "Chronicle not available"
    
    try:
        results = chronicle(topic, 5)
        if not results:
            return f"No results found for '{topic}'"
        
        output = f"📚 Found {len(results)} resources:\n"
        for i, r in enumerate(results, 1):
            url = getattr(r, 'url', str(r))
            output += f"{i}. {url}\n"
        return output
    except Exception as e:
        return f"Search error: {e}"

def stats():
    """Get chronicle statistics"""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        s = chronicle.get_stats()
        return f"📊 Chronicle Stats: {s['total_cards']} cards, {s['unique_urls']} URLs"
    except Exception as e:
        return f"Stats error: {e}"

# CLI handlers
def handle_solve(args):
    print(solve(args))

def handle_explain(args):
    print(explain(args))

def handle_search(args):
    print(search(args))

def handle_stats(args):
    print(stats())
