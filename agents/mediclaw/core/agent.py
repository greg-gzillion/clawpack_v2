"""Core Mediclaw Agent - Smart Webclaw Fetcher"""

import sys
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ROOT_PATH = Path("C:/Users/greg/dev/clawpack_v2")
sys.path.insert(0, str(ROOT_PATH))
from shared.llm.api import call

WEBCLAW_PATH = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/mediclaw")

# Priority domains for medical content
PRIORITY_DOMAINS = [
    "mayoclinic.org",
    "clevelandclinic.org",
    "cdc.gov",
    "nih.gov",
    "who.int",
    "heart.org",
    "uptodate.com",
    "pubmed.ncbi.nlm.nih.gov",
    "ama-assn.org"
]

class MediclawAgent:
    def __init__(self):
        self.session = {"queries": []}
    
    def _get_relevant_specialties(self, term):
        term_lower = term.lower()
        mapping = {
            "hypertension": ["cardiology", "diseases"],
            "blood pressure": ["cardiology"],
            "diabetes": ["endocrinology", "diseases"],
            "heart": ["cardiology"],
            "chest": ["cardiology", "emergency_medicine"],
            "cancer": ["oncology"],
            "arthritis": ["rheumatology"],
            "depression": ["psychiatry", "mental_health"],
        }
        for keyword, specialties in mapping.items():
            if keyword in term_lower:
                return specialties
        return None
    
    def _extract_urls(self, file_path, term):
        """Extract and rank URLs from markdown file based on relevance to term"""
        urls = []
        try:
            content = file_path.read_text(encoding='utf-8')
            term_lower = term.lower()
            
            # Find all URLs
            for url in re.findall(r'https?://[^\s\)\]]+', content):
                url = url.rstrip('.,;:!?)>')
                if url.startswith(('http://', 'https://')):
                    # Score URL relevance
                    score = 0
                    url_lower = url.lower()
                    
                    # Higher score for relevant domain content
                    if any(domain in url_lower for domain in ["cdc.gov", "mayoclinic", "clevelandclinic", "heart.org", "who.int"]):
                        score += 10
                    
                    # Higher score if term appears in URL path
                    if term_lower in url_lower:
                        score += 20
                    
                    # Higher score for specific paths (not just domain root)
                    parsed = urlparse(url)
                    if parsed.path and len(parsed.path) > 3:
                        score += 5
                    
                    urls.append({"url": url, "score": score})
        except:
            pass
        
        # Sort by score (highest first) and return URLs
        urls.sort(key=lambda x: x["score"], reverse=True)
        return [u["url"] for u in urls if u["score"] > 0][:5]
    
    def _fetch_url(self, url):
        """Fetch content from URL with better content extraction"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove non-content elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "ad"]):
                element.decompose()
            
            # Try to find main content area
            content_selectors = ['main', 'article', '.content', '#content', '.main-content', '.entry-content']
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                content = soup.body if soup.body else soup
            
            # Extract text and clean up
            text = content.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip() and len(line) > 30]
            
            # Get title
            title = soup.title.string if soup.title and soup.title.string else url
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "content": '\n'.join(lines[:40])[:2500]
            }
        except Exception as e:
            return {"success": False, "url": url, "error": str(e)}
    
    def _search_webclaw(self, term):
        """Search webclaw for relevant URLs"""
        term_lower = term.lower()
        target_specialties = self._get_relevant_specialties(term)
        
        all_urls = []
        specialties_to_search = target_specialties if target_specialties else [d.name for d in WEBCLAW_PATH.iterdir() if d.is_dir()]
        
        for specialty in specialties_to_search[:5]:  # Limit search
            specialty_path = WEBCLAW_PATH / specialty
            if specialty_path.exists():
                for md_file in specialty_path.glob("*.md"):
                    urls = self._extract_urls(md_file, term)
                    if urls:
                        all_urls.extend(urls)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in all_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        if unique_urls:
            return {"specialty": ", ".join(specialties_to_search[:3]), "urls": unique_urls[:4]}
        return None
    
    def _get_with_citations(self, term, context):
        match = self._search_webclaw(term)
        
        if match and match.get("urls"):
            output = f"📚 **WEBCLAW CITATIONS - {match['specialty'].upper()}**\n🔍 {term}\n\n"
            
            for url in match["urls"][:3]:
                result = self._fetch_url(url)
                if result["success"]:
                    output += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    output += f"📖 **{result['title'][:80]}**\n"
                    output += f"🔗 **Source:** {result['url']}\n\n"
                    output += f"**Excerpt:**\n{result['content']}\n\n"
                else:
                    output += f"❌ Could not fetch: {url}\n\n"
            
            output += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            return output
        else:
            # Fallback to AI
            ai_result = call(f"{context} for {term}. Provide evidence-based information with clinical recommendations.")
            return f"🤖 **AI RESPONSE**\n\n{ai_result}"
    
    def research(self, topic):
        return self._get_with_citations(topic, "Provide comprehensive medical research")
    
    def diagnose(self, symptoms):
        return self._get_with_citations(symptoms, "Provide differential diagnosis")
    
    def treatment(self, condition):
        return self._get_with_citations(condition, "Provide treatment guidelines")
    
    # Direct API commands
    def medications(self, drug):
        return call(f"Medication info for {drug}. Include dosing, side effects, contraindications.")
    
    def interactions(self, drugs):
        return call(f"Drug interactions for {drugs}.")
    
    def warnings(self, drug):
        return call(f"FDA warnings for {drug}.")
    
    def pediatrics(self, issue):
        return call(f"Pediatric info for {issue}.")
    
    def geriatrics(self, issue):
        return call(f"Geriatric info for {issue}.")
    
    def lab_tests(self, test):
        return call(f"Lab test interpretation for {test}.")
    
    def coding(self, diagnosis):
        return call(f"ICD-10 coding for {diagnosis}.")
    
    def prevention(self, condition):
        return call(f"Prevention guidelines for {condition}.")
    
    def diet(self, condition):
        return call(f"Dietary recommendations for {condition}.")
    
    def exercise(self, condition):
        return call(f"Exercise recommendations for {condition}.")
    
    def natural(self, condition):
        return call(f"Natural remedies for {condition}.")
    
    def procedure(self, name):
        return call(f"Procedure info for {name}.")
    
    def prognosis(self, condition):
        return call(f"Prognosis for {condition}.")
    
    def referral(self, condition):
        return call(f"Specialist referral for {condition}.")
    
    def webclaw_sources(self):
        if WEBCLAW_PATH.exists():
            return [d.name for d in WEBCLAW_PATH.iterdir() if d.is_dir()]
        return []
