"""Schedule language learning sessions for all agents"""
from language_learner_working import LanguageLearner

ll = LanguageLearner()

# What each agent should learn
learning_plan = {
    "lawclaw": ["Rust", "TypeScript", "Solidity", "Go"],
    "eagleclaw": ["Solidity", "Go", "TypeScript", "JavaScript", "C++"],
    "crustyclaw": ["TypeScript", "Go", "Python", "Solidity", "JavaScript"],
    "claw-coder": ["Rust", "TypeScript", "Go", "Solidity", "C++"],
    "claw-code": ["Python", "Rust", "Solidity", "Go", "JavaScript"]
}

print("ðŸŽ¯ STARTING LANGUAGE LEARNING")
print("="*50)

for agent, languages in learning_plan.items():
    print(f"\nðŸ“š {agent.upper()} LEARNING SESSION")
    for language in languages:
        current = ll.get_proficiency(agent, language)
        if current < 5:
            session = ll.start_learning_session(agent, language)
            result = ll.record_learning(agent, language, success=True)
            if result['improved']:
                print(f"   âœ… Learned {language}: level {current} â†’ {result['level']}")
            else:
                print(f"   ðŸ“– Practiced {language}: still level {current}")
        else:
            print(f"   â­ Already mastered {language}")

print("\n" + "="*50)
print("ðŸŽ‰ LEARNING SESSIONS COMPLETE!")

# Show final dashboard
ll.show_dashboard()
