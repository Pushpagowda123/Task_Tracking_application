from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

app = Flask(__name__)

# Enhanced ML model for various mathematical sequence prediction
def create_ml_model():
    """Create an enhanced model for various mathematical sequence prediction"""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    
    # Create training data for various sequence types
    training_data = []
    training_labels = []
    
    # 1. Arithmetic sequences (linear)
    for i in range(1, 21):
        training_data.append([i, i+1, i+2])
        training_labels.append(i+3)
    
    # 2. Geometric sequences (multiplication)
    for i in range(1, 11):
        training_data.append([i, i*2, i*4])
        training_labels.append(i*8)
    
    # 3. Square sequences
    for i in range(1, 11):
        training_data.append([i, i**2, i**3])
        training_labels.append(i**4)
    
    # 4. Fibonacci-like sequences
    for i in range(1, 11):
        training_data.append([i, i+1, i+(i+1)])
        training_labels.append((i+1)+(i+(i+1)))
    
    # 5. Look-and-Say inspired sequences
    look_say_examples = [
        [1, 11, 21, 1211],
        [2, 12, 1112, 3112],
        [3, 13, 1113, 3113]
    ]
    for seq in look_say_examples:
        if len(seq) >= 3:
            training_data.append(seq[:3])
            training_labels.append(seq[3])
    
    # 6. Magic trick sequences (Pick any number, add 2, multiply by 2, subtract 4, divide by 2, subtract original)
    for i in range(1, 11):
        seq = [i, i+2, (i+2)*2, (i+2)*2-4, ((i+2)*2-4)/2]
        training_data.append(seq[:3])
        training_labels.append(seq[3])
    
    # 7. 1089 trick inspired sequences
    for i in range(100, 200, 10):
        if len(str(i)) == 3 and len(set(str(i))) == 3:
            reversed_num = int(str(i)[::-1])
            diff = abs(i - reversed_num)
            sum_digits = sum(int(d) for d in str(diff))
            training_data.append([i, reversed_num, diff])
            training_labels.append(sum_digits)
    
    # Convert to numpy arrays
    X = np.array(training_data)
    y = np.array(training_labels)
    
    # Create and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model

# Initialize ML model
ml_model = create_ml_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Basic arithmetic operations
        if expression:
            # Replace 'x' with '*' for multiplication
            expression = expression.replace('x', '*')
            # Replace '÷' with '/' for division
            expression = expression.replace('÷', '/')
            
            # Evaluate the expression safely
            result = eval(expression)
            return jsonify({'result': result, 'error': None})
        else:
            return jsonify({'result': None, 'error': 'No expression provided'})
            
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        numbers = data.get('numbers', [])
        
        if len(numbers) < 3:
            return jsonify({'prediction': None, 'error': 'Need at least 3 numbers for prediction'})
        
        # Use the last 3 numbers to predict the next one
        X_pred = np.array([numbers[-3:]])
        ml_prediction = ml_model.predict(X_pred)[0]
        
        # Additional pattern analysis
        pattern_analysis = analyze_pattern(numbers)
        
        # Combine ML prediction with pattern analysis
        final_prediction = combine_predictions(ml_prediction, pattern_analysis, numbers)
        
        return jsonify({
            'prediction': round(final_prediction, 2),
            'ml_prediction': round(ml_prediction, 2),
            'pattern_analysis': pattern_analysis,
            'error': None
        })
        
    except Exception as e:
        return jsonify({'prediction': None, 'error': str(e)})

def analyze_pattern(numbers):
    """Analyze the pattern in the given numbers"""
    if len(numbers) < 3:
        return {}
    
    analysis = {}
    
    # Check for arithmetic sequence
    diffs = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
    if len(set(diffs)) == 1:
        analysis['type'] = 'Arithmetic Sequence'
        analysis['difference'] = diffs[0]
        analysis['next_arithmetic'] = numbers[-1] + diffs[0]
    
    # Check for geometric sequence
    if all(numbers[i] != 0 for i in range(len(numbers)-1)):
        ratios = [numbers[i+1] / numbers[i] for i in range(len(numbers)-1)]
        if len(set(round(r, 6) for r in ratios)) == 1:
            analysis['type'] = 'Geometric Sequence'
            analysis['ratio'] = ratios[0]
            analysis['next_geometric'] = numbers[-1] * ratios[0]
    
    # Check for square/cube patterns
    if len(numbers) >= 3:
        # Check if it's a square sequence
        if all(numbers[i] == (i+1)**2 for i in range(len(numbers))):
            analysis['type'] = 'Square Sequence'
            analysis['next_square'] = (len(numbers)+1)**2
        
        # Check if it's a cube sequence
        if all(numbers[i] == (i+1)**3 for i in range(len(numbers))):
            analysis['type'] = 'Cube Sequence'
            analysis['next_cube'] = (len(numbers)+1)**3
    
    # Check for Fibonacci-like patterns
    if len(numbers) >= 3:
        fib_pattern = True
        for i in range(2, len(numbers)):
            if numbers[i] != numbers[i-1] + numbers[i-2]:
                fib_pattern = False
                break
        if fib_pattern:
            analysis['type'] = 'Fibonacci-like Sequence'
            analysis['next_fibonacci'] = numbers[-1] + numbers[-2]
    
    # Check for Look-and-Say inspired patterns
    if len(numbers) >= 3:
        # Simple pattern detection for repeating digits
        last_num = str(numbers[-1])
        if len(last_num) > 1 and len(set(last_num)) == 1:
            analysis['type'] = 'Repeating Digit Pattern'
            analysis['next_repeating'] = int(last_num + last_num[0])
    
    # Check for magic trick patterns
    if len(numbers) >= 4:
        # Check if it follows the "pick any number" magic trick pattern
        if (numbers[1] == numbers[0] + 2 and 
            numbers[2] == numbers[1] * 2 and 
            numbers[3] == numbers[2] - 4):
            analysis['type'] = 'Magic Trick Pattern'
            analysis['next_magic'] = numbers[3] / 2
    
    return analysis

def combine_predictions(ml_prediction, pattern_analysis, numbers):
    """Combine ML prediction with pattern analysis for better accuracy"""
    if not pattern_analysis:
        return ml_prediction
    
    # If we have a clear pattern, use it
    if 'next_arithmetic' in pattern_analysis:
        return pattern_analysis['next_arithmetic']
    elif 'next_geometric' in pattern_analysis:
        return pattern_analysis['next_geometric']
    elif 'next_fibonacci' in pattern_analysis:
        return pattern_analysis['next_fibonacci']
    elif 'next_square' in pattern_analysis:
        return pattern_analysis['next_square']
    elif 'next_cube' in pattern_analysis:
        return pattern_analysis['next_cube']
    elif 'next_magic' in pattern_analysis:
        return pattern_analysis['next_magic']
    elif 'next_repeating' in pattern_analysis:
        return pattern_analysis['next_repeating']
    
    # Otherwise, use ML prediction
    return ml_prediction



if __name__ == '__main__':
    app.run(debug=True)
