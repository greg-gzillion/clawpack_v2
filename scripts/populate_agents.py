# Save this as scripts/populate_agents.py
import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references"
files = {}

# === CRUSTYCLAW ===
files["crustyclaw/README.md"] = """# CrustyClaw References - Rust Development
## Topics: Rust language, Cargo, compiler validation, systems programming, wasm
"""

# === DATACLAW ===
files["dataclaw/README.md"] = """# DataClaw References - Data Management & Search
## Topics: databases, data structures, indexing, search algorithms, ETL
"""

# === DESIGNCLAW ===
files["designclaw/README.md"] = """# DesignClaw References - Brand & Design
## Topics: graphic design, branding, HTML/CSS, logo design, design systems
"""

# === DRAFTCLAW ===
files["draftclaw/README.md"] = """# DraftClaw References - Technical Drawings
## Topics: blueprints, CAD, technical diagrams, schematics, engineering drawings
"""

# === DREAMCLAW ===
files["dreamclaw/README.md"] = """# DreamClaw References - AI Vision & Generation
## Topics: Stable Diffusion, image generation, computer vision, AI art
"""

# === FILECLAW ===
files["fileclaw/README.md"] = """# FileClaw References - File Operations
## Topics: file formats, parsers, import/export, data conversion, serialization
"""

# === PLOTCLAW ===
files["plotclaw/README.md"] = """# PlotClaw References - Data Visualization
## Topics: matplotlib, charts, graphs, data visualization, plotting
"""

# === RUSTYPYCRAW ===
files["rustypycraw/README.md"] = """# RustyPyCraw References - Python/Rust Interop
## Topics: PyO3, FFI, code analysis, AST parsing, cross-language optimization
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")