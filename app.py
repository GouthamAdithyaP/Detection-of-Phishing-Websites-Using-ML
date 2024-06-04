from flask import Flask, render_template, request
from features import extract_features
import joblib

app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load('XGBoostClassifier.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        url = request.form['url']
        # Extract features from the URL
        features = features(url)
        # Make prediction using the trained model
        prediction = model.predict([features])[0]
        if prediction == 0:
            result = "Phishing"
        else:
            result = "Legitimate"
        return render_template('index.html', result=result)

@app.route('/usecases')
def usecases():
     return 'usecases.html'

@app.route('/info')
def info():
     return 'info.html'

if __name__ == '__main__':
    app.run(debug=True)
