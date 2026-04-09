# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- **security@clawpack.dev** (preferred)
- Or use GitHub's private vulnerability reporting

You should receive a response within 48 hours. If the issue is confirmed:
- We'll release a patch as soon as possible
- You'll be credited in the security advisory (unless you prefer anonymity)

## Security Best Practices for Users

1. **API Keys**: Never commit API keys. Use `.env` files (see `.env.example`)
2. **Authentication**: Use environment variables for all credentials
3. **HTTPS**: All external API calls use HTTPS by default
4. **Input Validation**: All user inputs are sanitized

## Known Security Features

- ✅ Safe logging (no API key exposure)
- ✅ HTTPS enforcement for all API clients
- ✅ BeautifulSoup for safe HTML parsing
- ✅ Environment variable based configuration

## Responsible Disclosure

We follow the principle of responsible disclosure:
1. Report privately
2. Allow 90 days for fix before public disclosure
3. Coordinate disclosure timing
