"""Document Templates"""
TEMPLATES = {
    'letter': """[Date]

[Recipient Name]
[Company]
[Address]

Dear [Name],

[Message]

Sincerely,
[Your Name]""",

    'report': """# [Title]

## Executive Summary
[Summary]

## Findings
[Results]

## Recommendations
[Actions]""",

    'memo': """TO: [Recipients]
FROM: [Your Name]
DATE: [Date]
SUBJECT: [Subject]

[Body]""",

    'meeting_notes': """# Meeting: [Title]
Date: [Date]
Attendees: [Names]

## Notes
[Content]

## Actions
- [ ] Item 1
- [ ] Item 2"""
}

def get_template(name):
    return TEMPLATES.get(name, TEMPLATES['letter'])

def list_templates():
    return list(TEMPLATES.keys())
