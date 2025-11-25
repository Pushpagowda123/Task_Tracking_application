# 🤖 AI Calculator with Machine Learning

A modern calculator built with Python Flask that combines basic arithmetic operations with machine learning-powered number sequence prediction.

## Features

- **Basic Calculator**: Addition, subtraction, multiplication, division
- **Machine Learning**: Predict the next number in a sequence using linear regression
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Calculation History**: Keep track of your recent calculations
- **Keyboard Support**: Full keyboard navigation and input

## ML Functionality

The calculator includes a machine learning model that can predict the next number in a sequence. It uses a simple linear regression model trained on arithmetic sequences to make predictions.

**How it works:**
1. Enter 3 or more numbers in the ML section
2. Click "Predict Next Number"
3. The ML model analyzes the pattern and predicts the next number

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Project Structure

```
├── app.py              # Main Flask application
├── templates/
│   └── index.html     # Calculator interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **Flask**: Web framework
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning library
- **Werkzeug**: WSGI utilities

## Usage

### Basic Calculator
- Use the number buttons and operators to perform calculations
- Press `=` or `Enter` to calculate
- Press `C` or `Escape` to clear
- Use `Backspace` to delete last character

### ML Prediction
- Click the `ML` button to show the prediction section
- Enter at least 3 numbers in the sequence
- Click "Predict Next Number" to get the ML prediction

### Keyboard Shortcuts
- Numbers: `0-9`
- Operators: `+`, `-`, `*`, `/`
- Calculate: `Enter` or `=`
- Clear: `Escape`
- Delete: `Backspace`

## How the ML Model Works

The machine learning model uses linear regression to predict the next number in a sequence. It's trained on simple arithmetic sequences like:
- [1, 2, 3] → 4
- [2, 4, 6] → 8
- [3, 6, 9] → 12

The model learns patterns and can predict the next number for similar sequences you input.

## Customization

You can modify the ML model in `app.py`:
- Change the training data in `create_ml_model()`
- Use different ML algorithms from scikit-learn
- Add more sophisticated pattern recognition

## Troubleshooting

- **Port already in use**: Change the port in `app.py` or kill the existing process
- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **ML predictions not working**: Ensure you enter at least 3 numbers before prediction

## Future Enhancements

- Database storage for calculation history
- More advanced ML models (neural networks, time series)
- User accounts and personalized ML training
- API endpoints for external integration
- Mobile app version

## License

This project is open source and available under the MIT License.

