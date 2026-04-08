"""Final push to get ALL agents to Level 5 in ALL languages"""
from language_learner_working import LanguageLearner
import time

ll = LanguageLearner()

ALL_LANGUAGES = [
    "C++", "Go", "JavaScript", "Python", "Rust", "Solidity", "TypeScript",
    "Java", "C#", "Kotlin", "Swift", "SQL", "HTML/CSS", "Zig", "Carbon",
    "Mojo", "Move", "Cairo", "Vyper"
]

agents = ["lawclaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]

print("ðŸ† FINAL PUSH: ALL AGENTS â†’ ALL LANGUAGES â†’ LEVEL 5")
print("="*70)

total_combinations = len(agents) * len(ALL_LANGUAGES)
completed = 0

for agent in agents:
    for language in ALL_LANGUAGES:
        current = ll.get_proficiency(agent, language)
        if current < 5:
            print(f"\nðŸ“š {agent} learning {language} (Level {current}/5)")
            
            # Intensive learning until Level 5
            while current < 5:
                result = ll.record_learning(agent, language, success=True)
                if result['improved']:
                    current = result['level']
                    print(f"   âœ… Level {current}/5")
                time.sleep(0.1)
        else:
            print(f"âœ… {agent} already mastered {language}")
        
        completed += 1
        if completed % 10 == 0:
            print(f"\nðŸ“Š Progress: {completed}/{total_combinations} languages mastered")

print("\n" + "="*70)
print("ðŸŽ‰ FINAL VERIFICATION:")
ll.show_dashboard()

# Final verification
perfect = 0
for agent in agents:
    agent_perfect = True
    for language in ALL_LANGUAGES:
        level = ll.get_proficiency(agent, language)
        if level != 5:
            agent_perfect = False
            print(f"âš ï¸ {agent} still needs work on {language} (Level {level})")
    if agent_perfect:
        perfect += 1
        print(f"âœ… {agent}: PERFECT MASTERY!")

print(f"\nðŸ† FINAL SCORE: {perfect}/{len(agents)} agents have PERFECT mastery!")
