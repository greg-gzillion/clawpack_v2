# shared/court_rules_schema.py
"""
Court Local Rules Schema — canonical format for filing requirements.

Every court folder may contain a local_rules.md following this schema.
LawClaw reads these to generate jurisdiction-compliant filings via docuclaw.

Schema fields are optional — courts are scored by completeness percentage.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class CourtRules:
    """Complete local rules for a single court."""

    # ── Court Identity ──────────────────────────────────────────────────
    court_name: str = ""
    jurisdiction: str = ""  # e.g., "US District Court, Southern District of New York"
    division: str = ""  # e.g., "Manhattan"
    filing_system: str = ""  # "CM/ECF", "PACER", "eFileIL", etc.
    official_url: str = ""
    effective_date: str = ""
    last_verified: str = ""

    # ── Caption Requirements ────────────────────────────────────────────
    case_style_format: str = ""  # e.g., "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK"
    party_ordering: str = ""  # e.g., "Plaintiff(s) above Defendant(s)"
    docket_number_placement: str = ""  # e.g., "Right-aligned below case style"
    judge_assignment_display: str = ""  # e.g., "Left-aligned: Hon. [Judge Name], U.S.D.J."

    # ── Document Formatting ─────────────────────────────────────────────
    page_size: str = "8.5 x 11 inches"
    margins: str = "1 inch all sides"
    font_family: str = "Times New Roman or Courier"
    font_size: str = "12 point"
    line_spacing: str = "Double"
    paragraph_spacing: str = ""
    page_numbering: str = "Bottom center, starting at 1"
    footnote_rules: str = ""

    # ── Filing Constraints ──────────────────────────────────────────────
    max_file_size: str = ""  # e.g., "10 MB"
    accepted_formats: str = "PDF"
    bookmark_required: bool = False
    ocr_required: bool = False
    text_searchable_required: bool = True
    signature_requirements: str = "/s/ signature block or digital signature"

    # ── Motion Practice ─────────────────────────────────────────────────
    briefing_schedule: str = ""  # e.g., "Response 14 days, Reply 7 days"
    response_deadline_days: int = 0
    reply_deadline_days: int = 0
    page_limits: str = ""  # e.g., "Opening brief 25 pages, Reply 10 pages"
    word_limits: str = ""

    # ── Judge-Specific Preferences ──────────────────────────────────────
    standing_orders_url: str = ""
    chamber_copy_required: bool = False
    courtesy_copy_delivery: str = ""
    hearing_notice_requirements: str = ""
    citation_style_preferences: str = "Bluebook"

    # ── E-Filing Technical Rules ────────────────────────────────────────
    portal: str = ""  # e.g., "CM/ECF via PACER"
    login_required: bool = True
    service_requirements: str = "Electronic service via CM/ECF"
    emergency_filing_procedure: str = ""


def completeness_score(rules: CourtRules) -> Dict:
    """Score a court's rules by percentage of fields populated."""
    fields = [v for v in vars(rules).values() if isinstance(v, (str, bool, int))]
    total = len(fields)
    populated = sum(1 for v in fields if v)  # non-empty, non-zero, non-False
    return {
        "total_fields": total,
        "populated": populated,
        "percentage": round(populated / total * 100, 1),
        "grade": _grade(populated / total),
    }


def _grade(ratio: float) -> str:
    if ratio >= 0.80: return "A — Filing-ready"
    elif ratio >= 0.60: return "B — Caption-ready"
    elif ratio >= 0.40: return "C — Contact only"
    else: return "D — Skeletal"