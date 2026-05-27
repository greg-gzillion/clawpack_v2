from pathlib import Path

f = Path(r"C:\Users\greg\dev\clawpack_v2\agents\lawclaw\commands\docket.py")
c = f.read_text(encoding='utf-8', errors='ignore')

# Fix 1: Court code resolver for standard abbreviations
if 'court_code_map' not in c:
    court_map = '''
COURT_ABBREV = {
    "miwd": "W.D. Mich.",
    "nywd": "W.D.N.Y.",
    "tnwd": "W.D. Tenn.",
    "txwd": "W.D. Tex.",
    "ded": "D. Del.",
    "gand": "N.D. Ga.",
    "cand": "N.D. Cal.",
    "ilnd": "N.D. Ill.",
    "flsd": "S.D. Fla.",
    "nysd": "S.D.N.Y.",
    "caed": "E.D. Cal.",
    "paed": "E.D. Pa.",
    "mad": "D. Mass.",
    "cod": "D. Colo.",
    "azd": "D. Ariz.",
    "waed": "E.D. Wash.",
    "vaed": "E.D. Va.",
}
'''
    # Insert after imports
    c = c.replace('"""docket command', court_map + '\n"""docket command')

# Fix 2: Resolve court codes in display
old_court_display = 'court = r.get("court", "Unknown")'
new_court_display = '''court_url = r.get("court", "Unknown")
                court_code = court_url.rstrip("/").split("/")[-1] if court_url else ""
                court = COURT_ABBREV.get(court_code, court_url)'''
c = c.replace(old_court_display, new_court_display)

# Fix 3: Add ambiguity note and all-cases instruction
old_note = 'output.append(f"  Found {len(results)} matching cases:")'
new_note = '''output.append(f"  Found {len(results)} matching cases:")
            if len(results) > 1:
                output.append("  NOTE: Same docket number exists in multiple courts.")
                output.append("  Docket numbers are only unique within a single court.")'''
c = c.replace(old_note, new_note)

# Fix 4: Prompt requires ALL cases
old_prompt = 'prompt = f"""Summarize these CourtListener docket results.'
new_prompt = 'prompt = f"""Summarize ALL {len(docket_data)} cases below. Do not omit any cases.'
c = c.replace(old_prompt, new_prompt)

f.write_text(c, encoding='utf-8')
print("All polish applied")
