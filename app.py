"""
Password Strength Checker - Web Version
Flask web application with embedded HTML
"""

from flask import Flask, request, jsonify
from password_checker import PasswordChecker

app = Flask(__name__)
checker = PasswordChecker()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .header p {
            color: #666;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }

        input[type="password"],
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="password"]:focus,
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .toggle-password {
            margin-top: 10px;
        }

        .toggle-password label {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0;
            font-weight: 400;
            cursor: pointer;
        }

        .toggle-password input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        .strength-indicator {
            margin: 25px 0;
        }

        .strength-bar {
            height: 8px;
            background: #eee;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .strength-fill {
            height: 100%;
            width: 0%;
            transition: all 0.3s ease;
            border-radius: 4px;
        }

        .strength-text {
            font-weight: 600;
            font-size: 14px;
            text-align: center;
        }

        .weak { color: #e74c3c; }
        .fair { color: #f39c12; }
        .good { color: #3498db; }
        .excellent { color: #27ae60; }

        .checks-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 20px 0;
        }

        .check-item {
            padding: 12px;
            border-radius: 8px;
            background: #f8f9fa;
            border: 2px solid #ddd;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
        }

        .check-item.pass {
            background: #d4edda;
            border-color: #27ae60;
        }

        .check-item.fail {
            background: #f8d7da;
            border-color: #e74c3c;
        }

        .check-icon {
            font-size: 16px;
            min-width: 20px;
        }

        .recommendations {
            margin: 20px 0;
            padding: 15px;
            background: #fff3cd;
            border-left: 4px solid #f39c12;
            border-radius: 4px;
            display: none;
        }

        .recommendations.show {
            display: block;
        }

        .recommendations h3 {
            color: #f39c12;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .recommendations ul {
            list-style: none;
            padding-left: 0;
        }

        .recommendations li {
            color: #333;
            font-size: 13px;
            margin-bottom: 6px;
            padding-left: 20px;
            position: relative;
        }

        .recommendations li:before {
            content: "✗";
            position: absolute;
            left: 0;
            color: #e74c3c;
            font-weight: bold;
        }

        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #27ae60;
            display: none;
            margin: 20px 0;
        }

        .success-message.show {
            display: block;
        }

        .score-display {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin: 15px 0;
        }

        @media (max-width: 480px) {
            .checks-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Password Checker</h1>
            <p>Check your password strength in real-time</p>
        </div>

        <div class="form-group">
            <label for="password">Enter Password</label>
            <input type="password" id="password" placeholder="Enter your password...">
            <div class="toggle-password">
                <label>
                    <input type="checkbox" id="togglePassword">
                    Show password
                </label>
            </div>
        </div>

        <div class="strength-indicator" id="strengthIndicator" style="display: none;">
            <div class="strength-bar">
                <div class="strength-fill" id="strengthFill"></div>
            </div>
            <div class="strength-text">
                Strength: <span id="strengthText">Checking...</span>
            </div>
            <div class="score-display" id="scoreDisplay"></div>
        </div>

        <div class="checks-grid" id="checksGrid" style="display: none;"></div>

        <div class="success-message" id="successMessage">
            ✓ No issues found! This is a strong password.
        </div>

        <div class="recommendations" id="recommendations">
            <h3>Issues to Fix:</h3>
            <ul id="recommendationsList"></ul>
        </div>
    </div>

    <script>
        const passwordInput = document.getElementById('password');
        const togglePassword = document.getElementById('togglePassword');
        const strengthIndicator = document.getElementById('strengthIndicator');
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');
        const checksGrid = document.getElementById('checksGrid');
        const recommendations = document.getElementById('recommendations');
        const recommendationsList = document.getElementById('recommendationsList');
        const successMessage = document.getElementById('successMessage');
        const scoreDisplay = document.getElementById('scoreDisplay');

        // Toggle password visibility
        togglePassword.addEventListener('change', function() {
            passwordInput.type = this.checked ? 'text' : 'password';
        });

        // Check password on input
        passwordInput.addEventListener('input', async function() {
            const password = this.value;

            if (!password) {
                strengthIndicator.style.display = 'none';
                checksGrid.style.display = 'none';
                recommendations.classList.remove('show');
                successMessage.classList.remove('show');
                return;
            }

            try {
                const response = await fetch('/api/check', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ password: password })
                });

                const data = await response.json();

                // Show strength indicator
                strengthIndicator.style.display = 'block';
                checksGrid.style.display = 'grid';

                // Update strength bar
                const percentage = (data.score / 18) * 100;
                strengthFill.style.width = percentage + '%';

                // Set color based on strength
                let color;
                let strengthClass;
                if (data.strength.includes('Excellent')) {
                    color = '#27ae60';
                    strengthClass = 'excellent';
                } else if (data.strength.includes('Good')) {
                    color = '#3498db';
                    strengthClass = 'good';
                } else if (data.strength.includes('Fair')) {
                    color = '#f39c12';
                    strengthClass = 'fair';
                } else {
                    color = '#e74c3c';
                    strengthClass = 'weak';
                }

                strengthFill.style.backgroundColor = color;
                strengthText.textContent = data.strength;
                strengthText.className = strengthClass;
                scoreDisplay.textContent = data.score + '/18';

                // Update checks
                checksGrid.innerHTML = '';
                const checks = [
                    { label: 'Length (8+)', pass: data.password_length >= 8 },
                    { label: 'Uppercase', pass: data.has_uppercase },
                    { label: 'Lowercase', pass: data.has_lowercase },
                    { label: 'Numbers', pass: data.has_numbers },
                    { label: 'Special chars', pass: data.has_special },
                ];

                checks.forEach(check => {
                    const checkItem = document.createElement('div');
                    checkItem.className = 'check-item ' + (check.pass ? 'pass' : 'fail');
                    checkItem.innerHTML = `
                        <span class="check-icon">${check.pass ? '✓' : '✗'}</span>
                        <span>${check.label}</span>
                    `;
                    checksGrid.appendChild(checkItem);
                });

                // Update recommendations
                if (data.recommendations.length > 0) {
                    recommendations.classList.add('show');
                    successMessage.classList.remove('show');
                    recommendationsList.innerHTML = '';
                    data.recommendations.forEach(rec => {
                        const li = document.createElement('li');
                        li.textContent = rec;
                        recommendationsList.appendChild(li);
                    });
                } else {
                    recommendations.classList.remove('show');
                    successMessage.classList.add('show');
                }

            } catch (error) {
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    return HTML_TEMPLATE

@app.route('/api/check', methods=['POST'])
def check_password():
    """API endpoint to check password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({
            'error': 'Password is required',
            'score': 0,
            'strength': 'Empty'
        }), 400
    
    score, strength, details, recommendations = checker.analyze(password)
    
    return jsonify({
        'score': score,
        'strength': strength,
        'details': details,
        'recommendations': recommendations,
        'password_length': len(password),
        'has_uppercase': details['has_uppercase'],
        'has_lowercase': details['has_lowercase'],
        'has_numbers': details['has_numbers'],
        'has_special': details['has_special'],
    })

if __name__ == '__main__':
    print("\n🔐 Password Strength Checker is running!")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press CTRL+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
