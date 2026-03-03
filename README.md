# 🔐 Password Strength Checker

[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://password-strength-checker--muturawangari.replit.app)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive security-focused password validation tool built with Python. Features both a command-line interface and a modern web application.

## Features

- **Real-time password analysis** with instant feedback
- **Comprehensive security checks:**
  - Password length validation (minimum 8 characters recommended)
  - Character variety (uppercase, lowercase, numbers, special chars)
  - Sequential character detection (prevents patterns like "abc", "123")
  - Repeated character detection (prevents "aaa", "111")
  - Common password detection (checks against known weak passwords)
  
- **Detailed recommendations** - Gets specific advice on how to improve weak passwords
- **Two interfaces:**
  - **CLI (Command-line)** - For quick local testing
  - **Web UI** - Modern, user-friendly web interface with real-time feedback

## Architecture

This project demonstrates good software design with **separation of concerns**:

```
├── password_checker.py      # Core logic (reusable module)
├── cli_checker.py           # CLI interface
├── app.py                   # Flask web server
└── templates/
    └── index.html           # Web UI
```

The core `PasswordChecker` class can be imported and used anywhere, while the CLI and web versions consume it without duplicating logic.

## Installation

### Requirements
- Python 3.7+

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/password-strength-checker.git
cd password-strength-checker
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### CLI Version

Run the interactive command-line tool:

```bash
python cli_checker.py
```

Then enter passwords to check. The tool provides:
- Strength rating (Weak, Fair, Good, Excellent)
- Overall security score
- Detailed feedback on each criterion
- Specific recommendations for improvement

**Example:**
```
🔐 PASSWORD STRENGTH CHECKER 🔐
Enter password to check (or 'quit' to exit): 
Password: MyP@ssw0rd!
Strength: Excellent ✓✓ (Score: 15)
✓ No issues found! This is a strong password.
```

### Web Version

## 🌐 Live Demo

**Try it online:** 👉 **https://password-strength-checker--muturawangari.replit.app**

Just visit the link and start checking passwords instantly! No installation needed.

---

### Or Run Locally

To run on your own machine:
```bash
pip install -r requirements.txt
python app.py
```

Then open: **http://localhost:5000**

Features:
- Real-time password strength visualization
- Interactive strength bar with color coding
- Checkbox for each security criterion
- Live recommendations as you type
- Show/hide password toggle

## Security Scoring System

Passwords are scored out of 18 points based on:

| Criterion | Points | Details |
|-----------|--------|---------|
| Length | 0-3 | <8 chars (0), 8-12 (1), 12-16 (2), 16+ (3) |
| Uppercase | 2 | A-Z characters |
| Lowercase | 2 | a-z characters |
| Numbers | 2 | 0-9 digits |
| Special chars | 2 | !@#$%^&* etc. |
| No sequences | 2 | Avoids abc, 123 patterns |
| No repeats | 2 | Avoids aaa, 111 patterns |
| Not common | 2 | Not in weak password list |

**Strength Levels:**
- **Very Weak** (0-2 points): High security risk
- **Weak** (3-5 points): Poor security
- **Fair** (6-10 points): Acceptable but improvable
- **Good** (11-14 points): Strong password
- **Excellent** (15-18 points): Very strong password

## How It Works

### Core Checker Logic

The `PasswordChecker` class uses:

1. **Regex patterns** - Fast character matching
   - Uppercase: `[A-Z]`
   - Numbers: `[0-9]`
   - Special chars: `[!@#$%^&*...]`

2. **Sequential detection** - Finds patterns
   - Numbers: `012|123|234...`
   - Letters: Checks character ASCII values

3. **Dictionary comparison** - Against known weak passwords

### Example Usage in Code

```python
from password_checker import PasswordChecker

checker = PasswordChecker()
score, strength, details, recommendations = checker.analyze("MyP@ss123")

print(f"Strength: {strength}")
print(f"Score: {score}/18")
for rec in recommendations:
    print(f"- {rec}")
```

## Learning Outcomes

Building this project teaches:

- **Security best practices** - Understanding password security principles
- **Input validation** - Checking data against multiple criteria
- **Regex patterns** - Text matching and pattern detection
- **Code organization** - Separating business logic from UI
- **API design** - Creating reusable modules
- **Web development** - Flask basics and async API calls
- **CLI design** - User-friendly terminal applications
- **Testing** - Validating logic with test cases

## Security Notes

⚠️ **Important:** This tool is for educational and personal use:

- **Never send passwords over insecure connections** - This tool is designed to work locally
- **Always use HTTPS in production** - If deploying this publicly
- **Verify password strength locally** - Don't rely solely on external tools
- **Use a password manager** - For securely storing your passwords
- **Enable multi-factor authentication** - Even with strong passwords, MFA adds crucial security

## Future Enhancements

Ideas for extending this project:

- [ ] Database of more comprehensive weak passwords
- [ ] Entropy calculation using Shannon entropy
- [ ] Language-specific weak pattern detection
- [ ] Export results as JSON/PDF report
- [ ] Batch password checking from file
- [ ] HAVEIBEENPWNED API integration
- [ ] Docker containerization
- [ ] Dark mode for web UI
- [ ] Unit tests with pytest
- [ ] CI/CD pipeline with GitHub Actions

## Project Structure

```
password-strength-checker/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── password_checker.py          # Core module (no dependencies)
├── cli_checker.py              # CLI interface
├── app.py                      # Flask web server
├── templates/
│   └── index.html              # Web UI
└── .gitignore                  # Git ignore file
```

## Testing

Test with various passwords:

```python
from password_checker import PasswordChecker

checker = PasswordChecker()

test_cases = {
    "password": "Weak - common password",
    "Pass123": "Fair - has patterns",
    "MyP@ssw0rd!": "Good - strong password",
    "Tr0pic@lSunset#2024": "Excellent - very strong",
}

for pwd, expected in test_cases.items():
    score, strength, _, recs = checker.analyze(pwd)
    print(f"{pwd}: {strength}")
```

## Contributing

Feel free to fork and improve! Some ideas:
- Add more weak passwords to the common list
- Improve regex patterns
- Add language support
- Create unit tests
- Optimize performance

## License

MIT License - Feel free to use in your projects!

## Author

Created as a cybersecurity learning project.

---

**Made with 🔒 for cybersecurity education**
