"""Import CSV as markdown table"""
name = "/csvtable"

def run(args):
    if not args:
        print("Usage: /csvtable <file.csv>")
        return
    from pathlib import Path
    import csv
    p = Path(args)
    if not p.exists():
        print(f"File not found: {p}")
        return
    content = p.read_text()
    rows = list(csv.reader(content.split('\n')))
    if not rows:
        print("Empty CSV")
        return
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "|" + "|".join(["---" for _ in rows[0]]) + "|"
    body = "\n".join(["| " + " | ".join(row) + " |" for row in rows[1:] if row])
    table = f"{header}\n{sep}\n{body}"
    output = p.parent / f"{p.stem}_table.md"
    output.write_text(table)
    print(f"✅ CSV imported as table: {output}")
