"""Create a table"""
name = "/table"

def run(args):
    if not args:
        print("Usage: /table <rows>x<cols>")
        print("Example: /table 3x4")
        return
    from pathlib import Path
    parts = args.split('x')
    if len(parts) != 2:
        print("Format: /table 3x4")
        return
    rows, cols = int(parts[0]), int(parts[1])
    header = "| " + " | ".join([f"C{i+1}" for i in range(cols)]) + " |"
    sep = "|" + "|".join(["---" for _ in range(cols)]) + "|"
    body = "\n".join(["| " + " | ".join(["" for _ in range(cols)]) + " |" for _ in range(rows-1)])
    table = f"{header}\n{sep}\n{body}"
    output = Path(f"table_{rows}x{cols}.md")
    output.write_text(table)
    print(f"✅ Table saved to {output}")
