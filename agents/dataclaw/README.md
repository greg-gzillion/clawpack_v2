# DataClaw

Local data search and reference agent. Searches across all local files, structured data, and the chronicle index.

## Commands

| Command | Description |
|---------|-------------|
| `/search <query>` | Search local files and data |
| `/find <query>` | Same as /search |
| `/export <fmt> <query>` | Export search results |
| `/stats` | Index statistics |
| `/help` | Show commands |

## Search Locations

- `docs/` — documentation, papers, notes
- `data/` — structured data (JSON, CSV)
- `agents/webclaw/references/` — all reference files
- `exports/` — generated files

## File Format Support

For importing and processing specific file formats (PDF, DOCX, EPUB, images, etc.), use **DocuClaw** and **FileClaw**:
docuclaw: /import document.pdf — Import any supported format
docuclaw: /export pdf <content> — Export to any format
fileclaw: /convert pdf input.docx — Convert between formats

text

**Supported formats (via FileClaw):** pdf, docx, rtf, md, html, txt, xlsx, pptx, json, csv, yaml, toml, xml, ini, png, jpg, bmp, gif, tiff, webp, svg, zip

## Adding Local Files

Drop files into `docs/` or `data/` and DataClaw finds them by filename and text content on the next `/search`.

## A2A Integration

```python
self.call_agent("dataclaw", "/search machine learning papers")
self.call_agent("dataclaw", "/export json neural networks")