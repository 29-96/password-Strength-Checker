"""
Password Strength Checker
A security-focused password validation module
"""

import re
import string

class PasswordChecker:
    """Analyzes password strength and provides security recommendations"""
    
    def __init__(self):
        # Common weak passwords to check against
        self.common_passwords = {
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
            'baseball', '111111', 'iloveyou', 'master', 'sunshine',
            'ashley', 'bailey', 'passw0rd', '123123', '000000'
        }
    
    def check_length(self, password):
        """Check password length - security best practice"""
        length = len(password)
        if length < 8:
            return 0, "Password is too short (minimum 8 characters)"
        elif length < 12:
            return 1, "Password length is acceptable but could be longer"
        elif length < 16:
            return 2, "Good password length (12+ characters)"
        else:
            return 3, "Excellent password length (16+ characters)"
    
    def check_uppercase(self, password):
        """Check for uppercase letters"""
        if re.search(r'[A-Z]', password):
            return 2, "Contains uppercase letters ✓"
        return 0, "Missing uppercase letters - add A-Z"
    
    def check_lowercase(self, password):
        """Check for lowercase letters"""
        if re.search(r'[a-z]', password):
            return 2, "Contains lowercase letters ✓"
        return 0, "Missing lowercase letters - add a-z"
    
    def check_numbers(self, password):
        """Check for numeric characters"""
        if re.search(r'[0-9]', password):
            return 2, "Contains numbers ✓"
        return 0, "Missing numbers - add 0-9"
    
    def check_special_chars(self, password):
        """Check for special characters"""
        special_chars = string.punctuation  # !@#$%^&*()-_=+[]{}|;:'",.<>?/
        if re.search(f'[{re.escape(special_chars)}]', password):
            return 2, "Contains special characters ✓"
        return 0, "Missing special characters - add !@#$%^&* etc."
    
    def check_sequential_chars(self, password):
        """Detect sequential patterns like abc, 123, qwerty"""
        # Check for sequential numbers
        if re.search(r'012|123|234|345|456|567|678|789', password):
            return -1, "Contains sequential numbers (123, 456 etc.) - avoid these"
        
        # Check for sequential letters
        for i in range(len(password) - 2):
            if ord(password[i]) + 1 == ord(password[i+1]) and \
               ord(password[i+1]) + 1 == ord(password[i+2]):
                return -1, "Contains sequential letters (abc, xyz etc.) - avoid these"
        
        return 2, "No obvious sequential patterns ✓"
    
    def check_repeated_chars(self, password):
        """Detect repeated characters like aaa or 111"""
        if re.search(r'(.)\1{2,}', password):
            return -1, "Contains repeated characters (aaa, 111) - avoid these"
        return 2, "No excessive repeated characters ✓"
    
    def check_common_passwords(self, password):
        """Check against list of commonly used weak passwords"""
        if password.lower() in self.common_passwords:
            return -2, "This is a commonly used password - choose something unique"
        return 2, "Not a commonly used password ✓"
    
    def analyze(self, password):
        """
        Perform comprehensive password analysis
        Returns: (score, strength_level, details_dict, recommendations)
        """
        if not password:
            return 0, "Empty", {}, ["Enter a password to check"]
        
        # Run all checks
        checks = {
            'length': self.check_length(password),
            'uppercase': self.check_uppercase(password),
            'lowercase': self.check_lowercase(password),
            'numbers': self.check_numbers(password),
            'special_chars': self.check_special_chars(password),
            'sequential': self.check_sequential_chars(password),
            'repeated': self.check_repeated_chars(password),
            'common': self.check_common_passwords(password),
        }
        
        # Calculate total score
        total_score = sum(score for score, _ in checks.values())
        
        # Determine strength level
        if total_score <= 2:
            strength = "Very Weak ✗"
        elif total_score <= 5:
            strength = "Weak ✗"
        elif total_score <= 10:
            strength = "Fair ⚠"
        elif total_score <= 14:
            strength = "Good ✓"
        else:
            strength = "Excellent ✓✓"
        
        # Collect recommendations (negative scores are critical)
        recommendations = []
        for check_name, (score, message) in checks.items():
            if score < 0:
                recommendations.insert(0, message)  # Critical issues first
            elif score == 0:
                recommendations.append(message)  # Then improvements
        
        # Create detailed report
        details = {
            'score': total_score,
            'strength': strength,
            'checks': {name: message for name, (_, message) in checks.items()},
            'password_length': len(password),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_numbers': bool(re.search(r'[0-9]', password)),
            'has_special': bool(re.search(f'[{re.escape(string.punctuation)}]', password)),
        }
        
        return total_score, strength, details, recommendations


# Example usage / testing
if __name__ == "__main__":
    checker = PasswordChecker()
    
    test_passwords = [
        "password",
        "Pass123",
        "MyP@ssw0rd!",
        "Tr0pic@lSunset#2024",
    ]
    
    for pwd in test_passwords:
        score, strength, details, recommendations = checker.analyze(pwd)
        print(f"\nPassword: {pwd}")
        print(f"Strength: {strength} (Score: {score})")
        print("Issues to fix:")
        for rec in recommendations:
            print(f"  - {rec}")
