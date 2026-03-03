#!/usr/bin/env python3
"""
Password Strength Checker - CLI Version
Command-line interface for checking password strength
"""

import sys
from password_checker import PasswordChecker
import getpass

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print application header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}")
    print("🔐 PASSWORD STRENGTH CHECKER 🔐")
    print(f"{'='*50}{Colors.END}\n")

def get_strength_color(strength):
    """Return color code based on strength level"""
    if "Excellent" in strength:
        return Colors.GREEN
    elif "Good" in strength:
        return Colors.CYAN
    elif "Fair" in strength:
        return Colors.YELLOW
    else:
        return Colors.RED

def display_results(score, strength, details, recommendations):
    """Display password analysis results in a user-friendly format"""
    
    strength_color = get_strength_color(strength)
    
    print(f"\n{Colors.BOLD}ANALYSIS RESULTS{Colors.END}")
    print(f"{Colors.BOLD}{'─'*50}{Colors.END}")
    
    print(f"\nStrength Level: {strength_color}{Colors.BOLD}{strength}{Colors.END}")
    print(f"Overall Score: {score}/18")
    
    # Progress bar
    bar_length = 30
    filled = int((score / 18) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"Progress: [{bar}] {int((score/18)*100)}%")
    
    # Detailed checks
    print(f"\n{Colors.BOLD}Detailed Checks:{Colors.END}")
    for check_name, message in details['checks'].items():
        # Format check name nicely
        display_name = check_name.replace('_', ' ').title()
        print(f"  {display_name}: {message}")
    
    # Recommendations
    if recommendations:
        print(f"\n{Colors.BOLD}Issues to Fix:{Colors.END}")
        for i, rec in enumerate(recommendations, 1):
            if any(word in rec for word in ['avoid', 'Missing', 'commonly']):
                color = Colors.RED
            else:
                color = Colors.YELLOW
            print(f"  {color}✗{Colors.END} {rec}")
    else:
        print(f"\n{Colors.GREEN}✓ No issues found! This is a strong password.{Colors.END}")
    
    print()

def main():
    """Main CLI application loop"""
    print_header()
    checker = PasswordChecker()
    
    print(f"{Colors.BOLD}How to use:{Colors.END}")
    print("1. Enter a password to check its strength")
    print("2. Get detailed feedback and improvement suggestions")
    print("3. Type 'quit' or 'exit' to exit\n")
    
    while True:
        try:
            # Get password input (hidden)
            password = getpass.getpass(f"{Colors.BLUE}Enter password to check (or 'quit' to exit): {Colors.END}")
            
            if password.lower() in ['quit', 'exit']:
                print(f"\n{Colors.CYAN}Thank you for using Password Strength Checker!{Colors.END}\n")
                break
            
            if not password:
                print(f"{Colors.YELLOW}Please enter a password.{Colors.END}\n")
                continue
            
            # Analyze password
            score, strength, details, recommendations = checker.analyze(password)
            
            # Display results
            display_results(score, strength, details, recommendations)
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}Exited. Goodbye!{Colors.END}\n")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}\n")

if __name__ == "__main__":
    main()
