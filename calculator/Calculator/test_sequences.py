#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced ML model's sequence prediction capabilities
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor

def create_enhanced_ml_model():
    """Create the enhanced ML model for sequence prediction"""
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
    
    # 6. Magic trick sequences
    for i in range(1, 11):
        seq = [i, i+2, (i+2)*2, (i+2)*2-4, ((i+2)*2-4)/2]
        training_data.append(seq[:3])
        training_labels.append(seq[3])
    
    # Convert to numpy arrays
    X = np.array(training_data)
    y = np.array(training_labels)
    
    # Create and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model

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
    
    # Check for magic trick patterns
    if len(numbers) >= 4:
        if (numbers[1] == numbers[0] + 2 and 
            numbers[2] == numbers[1] * 2 and 
            numbers[3] == numbers[2] - 4):
            analysis['type'] = 'Magic Trick Pattern'
            analysis['next_magic'] = numbers[3] / 2
    
    return analysis

def test_sequences():
    """Test various mathematical sequences"""
    print("🧠 Enhanced ML Model - Sequence Prediction Test")
    print("=" * 50)
    
    # Create the model
    model = create_enhanced_ml_model()
    
    # Test sequences
    test_cases = [
        ([1, 2, 3], "Arithmetic Sequence"),
        ([2, 4, 8], "Geometric Sequence"),
        ([1, 1, 2], "Fibonacci-like Sequence"),
        ([1, 4, 9], "Square Sequence"),
        ([5, 7, 14, 10], "Magic Trick Pattern"),
        ([3, 6, 9], "Arithmetic Sequence"),
        ([1, 3, 9], "Geometric Sequence"),
        ([2, 3, 5], "Fibonacci-like Sequence"),
        ([1, 8, 27], "Cube Sequence"),
        ([10, 12, 24, 20], "Magic Trick Pattern")
    ]
    
    for numbers, expected_type in test_cases:
        print(f"\n📊 Testing: {numbers} (Expected: {expected_type})")
        
        # ML prediction
        if len(numbers) >= 3:
            X_pred = np.array([numbers[-3:]])
            ml_prediction = model.predict(X_pred)[0]
            print(f"   🤖 ML Prediction: {ml_prediction:.2f}")
        
        # Pattern analysis
        pattern_analysis = analyze_pattern(numbers)
        if pattern_analysis:
            print(f"   🔍 Pattern Detected: {pattern_analysis['type']}")
            if 'next_arithmetic' in pattern_analysis:
                print(f"      Next (Arithmetic): {pattern_analysis['next_arithmetic']}")
            elif 'next_geometric' in pattern_analysis:
                print(f"      Next (Geometric): {pattern_analysis['next_geometric']}")
            elif 'next_fibonacci' in pattern_analysis:
                print(f"      Next (Fibonacci): {pattern_analysis['next_fibonacci']}")
            elif 'next_square' in pattern_analysis:
                print(f"      Next (Square): {pattern_analysis['next_square']}")
            elif 'next_cube' in pattern_analysis:
                print(f"      Next (Cube): {pattern_analysis['next_cube']}")
            elif 'next_magic' in pattern_analysis:
                print(f"      Next (Magic): {pattern_analysis['next_magic']}")
        else:
            print("   ❌ No clear pattern detected")

if __name__ == "__main__":
    test_sequences()

