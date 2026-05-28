from pathlib import Path

f = Path(r"C:\Users\greg\dev\clawpack_v2\agents\lawclaw\commands\federal.py")
c = f.read_text(encoding="utf-8", errors="ignore")

# The issue: SDNY exact match should work but the generic fallback 
# is running first. Let me check if the district check is even being reached.
# Problem might be the circuit check block running when "sdny" is passed.

# Let me add debug to trace the flow
old_circ_check = '''if circuit_num:
            c = CIRCUITS[circuit_num]'''

new_circ_check = '''if circuit_num and circuit_num != "fc" and circuit_num != "dc":
            c = CIRCUITS[circuit_num]'''

# Actually the real issue: the "dc" circuit matches "dc" in "sdny"? No, args_lower is "sdny".
# Let me just check: does the circuit loop find anything for "sdny"?
# The circuit loop looks for num in args_lower where num is "1","2",..."dc","fc"
# None of those are in "sdny" except... no, none are.

# The actual issue must be that the file saved didn't update properly.
# Let me check the actual content around line 80-100:

# Print relevant section
lines = c.split('\n')
for i, line in enumerate(lines[75:115], start=76):
    if 'district' in line.lower() or 'DISTRICT' in line:
        print(f"  {i}: {line}")

