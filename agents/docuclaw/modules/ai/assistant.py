"""AI Assistant Module - With Active Chronicle Learning & References"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root
PROJECT_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(PROJECT_ROOT))

class AIAssistant:
    def __init__(self):
        self.llm = None
        self.chronicle = None
        self._init_llm()
        self._init_chronicle()
        self.learning_memory = []
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            llm_manager = get_llm_manager()
            if llm_manager and hasattr(llm_manager, 'groq_client') and llm_manager.groq_client:
                self.llm = llm_manager
                print("✅ Groq Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ LLM error: {e}", file=sys.stderr)
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def search_index(self, topic, doc_type, max_results=5):
        """Search chronicle for relevant references"""
        if not self.chronicle:
            return []
        
        # Search variations for better results
        search_terms = [
            topic,
            doc_type,
            f"{doc_type} template",
            f"professional {doc_type}",
            f"business {doc_type}",
            "document best practices"
        ]
        
        all_results = []
        seen_urls = set()
        
        for term in search_terms[:4]:
            try:
                results = self.chronicle(term, 3)
                for r in results:
                    url = getattr(r, 'url', str(r))
                    source = getattr(r, 'source', 'chronicle')
                    if url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append({
                            'url': url,
                            'source': source,
                            'term': term
                        })
            except:
                pass
        
        return all_results[:max_results]
    
    def learn_from_past(self, doc_type):
        """Learn from previously generated documents in the index"""
        if not self.chronicle:
            return []
        
        try:
            # Search for past documents of same type
            results = self.chronicle(f"{doc_type} document", 5)
            learned = []
            for r in results:
                learned.append({
                    'url': getattr(r, 'url', str(r)),
                    'source': getattr(r, 'source', 'unknown'),
                    'type': doc_type
                })
            if learned:
                print(f"📚 Learned from {len(learned)} past documents", file=sys.stderr)
            return learned
        except:
            return []
    
    def generate(self, topic, doc_type):
        """Generate document using LLM with chronicle references and learning"""
        
        # 1. Search chronicle for relevant references
        references = self.search_index(topic, doc_type)
        
        # 2. Learn from past documents
        past_docs = self.learn_from_past(doc_type)
        
        # Build reference section for the prompt
        ref_section = ""
        if references:
            ref_section = "\n\n## Reference Sources (from Chronicle Index)\n"
            for i, ref in enumerate(references[:5], 1):
                ref_section += f"{i}. {ref['url']}\n"
            ref_section += "\nUse these as inspiration and follow best practices.\n"
        
        # Add learning section
        learning_section = ""
        if past_docs:
            learning_section = f"\n## Learning from Past Documents\n"
            learning_section += f"I have analyzed {len(past_docs)} previous {doc_type} documents.\n"
            learning_section += "Apply successful patterns and avoid common issues.\n"
        
        # Type-specific prompt with references
        prompts = {
            'letter': f"""Write a professional business letter about: {topic}

{ref_section}
{learning_section}

The letter must include:
- Date line
- Recipient information
- Subject line
- Professional salutation
- 3-4 meaningful paragraphs with specific details
- Professional closing
- Placeholders in [brackets] for personalization

Return ONLY the letter content.""",

            'report': f"""Write a professional business report about: {topic}

{ref_section}
{learning_section}

Include:
- Executive Summary
- Key Findings with data
- Analysis
- Recommendations
- Conclusion

Return ONLY the report content.""",

            'memo': f"""Write a professional memo about: {topic}

{ref_section}
{learning_section}

Include:
- TO:, FROM:, DATE:, SUBJECT:
- Background
- Discussion
- Action Items with owners
- Timeline

Return ONLY the memo content.""",

            'meeting_notes': f"""Write meeting notes about: {topic}

{ref_section}
{learning_section}

Include:
- Date and attendees
- Agenda
- Discussion summary
- Decisions made
- Action items with owners and due dates
- Next meeting date

Return ONLY the meeting notes."""
        }
        
        prompt = prompts.get(doc_type, prompts['letter'])
        
        if not self.llm:
            return self._fallback(topic, doc_type)
        
        try:
            response = self.llm.chat_sync(prompt, task_type="writing")
            if response and len(response) > 100:
                # Add citation footer if references were used
                if references or past_docs:
                    footer = f"\n\n---\n*Generated by DocuClaw AI*"
                    if references:
                        footer += f"\n*📚 References: {len(references)} sources from chronicle index*"
                    if past_docs:
                        footer += f"\n*📖 Learning: Analyzed {len(past_docs)} past documents*"
                    response += footer
                return response
        except Exception as e:
            print(f"⚠️ Generation error: {e}", file=sys.stderr)
        
        return self._fallback(topic, doc_type)
    
    def save_to_memory(self, doc_type, content, topic):
        """Save generated document to chronicle for future learning"""
        if not self.chronicle:
            return
        
        try:
            # In a real implementation, this would save to chronicle
            # For now, we'll just track in memory
            self.learning_memory.append({
                'type': doc_type,
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'length': len(content)
            })
            print(f"💾 Saved to memory: {doc_type} about {topic}", file=sys.stderr)
        except:
            pass
    
    def _fallback(self, topic, doc_type):
        return f"# {doc_type.title()}: {topic}\n\nLLM connection issue. Please check configuration."
    
    def is_available(self):
        return self.llm is not None
    
    def get_chronicle_stats(self):
        """Get statistics about the chronicle index"""
        if not self.chronicle:
            return "Chronicle not connected"
        
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            stats = chronicle.get_stats()
            return {
                'total_cards': stats.get('total_cards', 0),
                'unique_urls': stats.get('unique_urls', 0),
                'categories': len(stats.get('sources', {}))
            }
        except:
            return "Unable to get stats"

if __name__ == "__main__":
    ai = AIAssistant()
    print(f"LLM Available: {ai.is_available()}")
    print(f"Chronicle Available: {ai.chronicle is not None}")
    
    stats = ai.get_chronicle_stats()
    if isinstance(stats, dict):
        print(f"Chronicle Stats: {stats['total_cards']} cards, {stats['unique_urls']} URLs")
    
    if ai.is_available():
        print("\nGenerating document with chronicle learning...")
        result = ai.generate("Strategic Partnership", "letter")
        print("\n" + "="*60)
        print(result[:500])
        print("="*60)
