# 🗂️ FileClaw - Universal File Handler

**Purpose:** Centralized file import/export/conversion service for all ClawPack agents via A2A.

## 📦 Supported Formats (41+)

### Document Import
| Format | Extension | Capability |
|--------|-----------|------------|
| PDF | .pdf | Full text extraction (all pages) |
| Word | .docx | Paragraph text extraction |
| Excel | .xlsx | All sheets as text tables |
| PowerPoint | .pptx | Slide text extraction |
| Rich Text | .rtf | Basic text extraction |

### Image Import
| Format | Extension | Capability |
|--------|-----------|------------|
| PNG, JPG, GIF, BMP, WebP, SVG | .png .jpg .gif .bmp .webp .svg | Metadata, dimensions, EXIF |

### Archive Import
| Format | Extension | Capability |
|--------|-----------|------------|
| ZIP | .zip | List contents with sizes |
| TAR/GZ | .tar .gz | List contents with sizes |

### Media Import
| Format | Extension | Capability |
|--------|-----------|------------|
| MP3, WAV | .mp3 .wav | Metadata (use external tools for playback) |
| MP4, MPEG, MKV, AVI, MOV | .mp4 .mpeg .mkv .avi .mov | Metadata only |

### Text Formats (27 types)
Read/write: .md .txt .html .xml .json .csv .yaml .yml .toml .ini .cfg .py .js .ts .rs .go .cpp .c .java .rb .php .css .sql .r .sh .bat .ps1

## 📤 Export Formats
- **Markdown** (.md)
- **HTML** (.html) - auto-wrapped with styling
- **Plain Text** (.txt)
- **JSON** (.json) - pretty-printed
- **CSV** (.csv) - from JSON arrays
- **XML** (.xml)

## 🔄 Conversion
Convert between any supported import format → any export format:
/convert data.csv json # CSV to JSON
/convert report.md html # Markdown to HTML
/convert data.json csv # JSON to CSV

text

## 📦 Dependencies

`ash
pip install pypdf python-docx openpyxl pandas python-pptx pillow
Optional (for enhanced features):

bash
pip install pdfplumber markdown pyrtf3
🔗 A2A Integration
Any agent can call FileClaw through A2A:

python
# Import a file for analysis
requests.post("http://127.0.0.1:8766/v1/message/fileclaw",
    json={"task": "/import /path/to/document.pdf"})

# Export agent output to file
requests.post("http://127.0.0.1:8766/v1/message/fileclaw",
    json={"task": "/export html <h1>Results</h1>"})

# Convert between formats
requests.post("http://127.0.0.1:8766/v1/message/fileclaw",
    json={"task": "/convert data.csv json"})
📋 Commands
CommandDescription
/import <path>Read any supported file
/export <fmt> <content>Save content to file
/convert <src> <fmt>Convert file between formats
/helpShow this help
/statsShow agent statistics
🏗️ Architecture
text
FileClaw Agent (BaseAgent)
├── IMPORT: Binary readers (PDF, DOCX, XLSX, PPTX, images, archives, media)
├── IMPORT: Text readers (27 code/text formats)
├── EXPORT: Format writers (MD, HTML, TXT, JSON, CSV, XML)
├── CONVERT: Import → Export pipeline
└── A2A: Exposed to all 21 agents via a2a_server.py
📁 Output Location
All exports saved to: clawpack_v2/exports/
