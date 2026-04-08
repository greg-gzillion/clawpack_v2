"""Help command - show all WebClaw commands"""

def help_command(args=None):
    from utils import display_banner, display_categories, display_commands
    
    display_banner("WEBCLAW - WEB RESEARCH & SECURITY", "🌐")
    
    categories = [
        "Cloud Architecture", "AWS", "Azure", "GCP", "Kubernetes",
        "Docker", "Network Security", "Cybersecurity", "DevOps", "Terraform",
        "Infrastructure", "Monitoring", "Logging", "Compliance", "Identity Management",
        "Penetration Testing", "Malware Analysis", "Incident Response", "Serverless"
    ]
    
    display_categories(categories)
    
    all_commands = [
        ("/stats", "System statistics"),
        ("/list", "List categories"),
        ("/search", "Search references"),
        ("/browse", "Browse category"),
        ("/fetch", "Fetch URL"),
        ("/llm", "AI questions"),
        ("/share", "Query all agents"),
        ("/recall", "Recall memory"),
        ("/help", "This help"),
        ("/quit", "Exit")
    ]
    
    display_commands(all_commands)
    
    print("\n💡 TIPS:")
    print("  • Ask natural language questions about web/cloud/security")
    print("  • Use /search for specific keywords")
    print("  • Use /browse to explore categories")
    print("  • Use /share to learn from other agents")
    print("="*80)
