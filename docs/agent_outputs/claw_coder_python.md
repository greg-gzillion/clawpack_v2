# claw_coder: /code python function to validate email addresses

Saved: python_function_to_validate_email_addresses_20260601_201851.py | Validated: Syntax OK

```python
import re

def validate_email(email: str) -> bool:
    """
    Validates an email address using a regular expression.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
```