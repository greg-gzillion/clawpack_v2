#!/usr/bin/env python3
"""DocuClaw - Modular Document Processor"""

import sys
import webbrowser
from pathlib import Path
from datetime import datetime

# Import modules
from modules.ai.assistant import AIAssistant
from modules.formatter.styles import Formatter
from modules.templates.docs import get_template, list_templates
from modules.media.handler import MediaHandler
from modules.export.handler import ExportHandler

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class DocuClaw:
    def __init__(self):
        self.ai = AIAssistant()
        self.formatter = Formatter()
        self.media = MediaHandler()
        self.exporter = ExportHandler()
    
    def create(self, template_name, use_ai=False, topic=""):
        """Create a document from template"""
        if template_name not in list_templates():
            return f"❌ Unknown template. Available: {', '.join(list_templates())}"
        
        if use_ai and topic:
            content = self.ai.generate(topic, template_name)
        else:
            content = get_template(template_name)
            
            # Simple placeholder replacement
            print(f"\n📝 Creating '{template_name}' document...")
            for placeholder in ['Date', 'Name', 'Message', 'Title', 'Summary', 'Body']:
                val = input(f"  {placeholder}: ").strip()
                if val:
                    content = content.replace(f'[{placeholder}]', val)
        
        # Apply formatting
        styled = self.formatter.apply(content, 'professional')
        
        # Save
        filename = OUTPUT_DIR / f"{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filename.write_text(styled)
        webbrowser.open(f'file://{filename}')
        
        return f"✅ Document created: {filename}"
    
    def ai_create(self, topic, doc_type="letter"):
        """AI-powered document creation"""
        content = self.ai.generate(topic, doc_type)
        styled = self.formatter.apply(content, 'professional')
        filename = OUTPUT_DIR / f"ai_{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filename.write_text(styled)
        webbrowser.open(f'file://{filename}')
        return f"✅ AI document created: {filename}"
    
    def improve(self, file_path):
        """Improve existing document with AI"""
        path = Path(file_path)
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        original = path.read_text()
        improved = self.ai.improve(original)
        styled = self.formatter.apply(improved, 'professional')
        filename = OUTPUT_DIR / f"improved_{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filename.write_text(styled)
        webbrowser.open(f'file://{filename}')
        return f"✅ Document improved: {filename}"
    
    def import_media(self, file_path):
        """Import image or data file"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix in ['.png', '.jpg', '.jpeg', '.gif']:
            result = self.media.import_image(file_path)
            if result:
                return f"✅ Image imported: {result['path']}\nEmbed: {result['embed']}"
        elif suffix == '.csv':
            result = self.media.import_csv(file_path)
            if result:
                return f"✅ CSV imported: {result['rows']} rows, {', '.join(result['columns'])}"
        
        return f"❌ Unsupported or not found: {file_path}"
    
    def list_styles(self):
        return f"Styles: {', '.join(self.formatter.list_styles())}"
    
    def list_templates(self):
        return f"Templates: {', '.join(list_templates())}"
    
    def interactive(self):
        """Interactive mode"""
        print("\n🤖 DocuClaw Interactive Mode")
        print("Commands: create <template> | ai <topic> | improve <file> | import <file> | help | quit")
        
        while True:
            try:
                cmd = input("\n📄 docuclaw> ").strip().lower()
                if not cmd:
                    continue
                if cmd in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                parts = cmd.split(maxsplit=1)
                if parts[0] == 'create' and len(parts) > 1:
                    print(self.create(parts[1]))
                elif parts[0] == 'ai' and len(parts) > 1:
                    print(self.ai_create(parts[1]))
                elif parts[0] == 'improve' and len(parts) > 1:
                    print(self.improve(parts[1]))
                elif parts[0] == 'import' and len(parts) > 1:
                    print(self.import_media(parts[1]))
                elif parts[0] == 'styles':
                    print(self.list_styles())
                elif parts[0] == 'templates':
                    print(self.list_templates())
                elif cmd == 'help':
                    print(self.help())
                else:
                    print("Unknown. Try: create letter, ai report, improve file.md, import image.png")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════╗
║                    DOCUCLAW - Modular Document Processor     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  COMMANDS:                                                   ║
║    create <template>     - Create document from template    ║
║    ai <topic> [type]     - AI-generated document            ║
║    improve <file>        - AI-improve existing document     ║
║    import <file>         - Import image or CSV              ║
║    styles                - List formatting styles           ║
║    templates             - List document templates          ║
║    interactive           - Start interactive mode           ║
║                                                              ║
║  TEMPLATES: letter, report, memo, meeting_notes             ║
║  STYLES: professional, modern, academic, business           ║
║                                                              ║
║  EXAMPLES:                                                   ║
║    python docuclaw.py create letter                         ║
║    python docuclaw.py ai "Quarterly Report" report          ║
║    python docuclaw.py improve mydoc.md                      ║
║    python docuclaw.py import diagram.png                    ║
║    python docuclaw.py interactive                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
    
    def process(self, cmd, *args):
        if cmd == "create" and args:
            return self.create(args[0])
        elif cmd == "ai" and args:
            doc_type = args[1] if len(args) > 1 else "letter"
            return self.ai_create(args[0], doc_type)
        elif cmd == "improve" and args:
            return self.improve(args[0])
        elif cmd == "import" and args:
            return self.import_media(args[0])
        elif cmd == "styles":
            return self.list_styles()
        elif cmd == "chronicle-stats":
            return self.chronicle_stats()
        elif cmd == "templates":
            return self.list_templates()
        elif cmd == "interactive":
            self.interactive()
            return ""
        else:
            return self.help()

def main():
    agent = DocuClaw()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    if result:
        print(result)

if __name__ == "__main__":
    main()

    def chronicle_stats(self):
        """Show chronicle index statistics"""
        stats = self.ai.get_chronicle_stats()
        if isinstance(stats, dict):
            return f"""
📊 CHRONICLE INDEX STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Total Cards: {stats['total_cards']}
🔗 Unique URLs: {stats['unique_urls']}
🏷️  Categories: {stats['categories']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 DocuClaw will learn from and reference these sources
"""
        return f"Chronicle stats: {stats}"

    def chronicle_stats(self):
        """Show chronicle index statistics"""
        if not hasattr(self, 'ai'):
            self.ai = AIAssistant()
        stats = self.ai.get_chronicle_stats()
        if isinstance(stats, dict):
            return f"""
📊 CHRONICLE INDEX STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Total Cards: {stats['total_cards']}
🔗 Unique URLs: {stats['unique_urls']}
🏷️  Categories: {stats['categories']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 DocuClaw learns from and references these sources
"""
        return f"Chronicle stats: {stats}"
