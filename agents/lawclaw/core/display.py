"""Display utilities"""

class Display:
    @staticmethod
    def banner():
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*18 + "⚖️  LAWCLAW - JUDICIAL RESEARCH  ⚖️" + " "*18 + "█")
        print("█" + " "*78 + "█")
        print("█"*80)
    
    @staticmethod
    def categories():
        print("\n" + "="*80)
        print("📚 LAW CATEGORIES")
        print("="*80)
        cats = ["Constitutional", "Criminal", "Civil", "Family", "Corporate",
                "Tax", "Employment", "Immigration", "Bankruptcy", "Property",
                "Contract", "Tort", "Administrative", "Environmental", "Health"]
        for i, c in enumerate(cats):
            if i % 5 == 0 and i > 0:
                print()
            print(f"  • {c:<18}", end="")
        print("\n" + "="*80)
    
    @staticmethod
    def commands(cmd_list):
        print("\n🎯 COMMANDS")
        print("="*80)
        for i, cmd in enumerate(sorted(cmd_list)):
            if i % 4 == 0 and i > 0:
                print()
            print(f"  {cmd:<18}", end="")
        print("\n" + "="*80)
