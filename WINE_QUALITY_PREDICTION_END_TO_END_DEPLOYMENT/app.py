from flask import Flask, render_template, request
import os
import numpy as np
from src.datascience.pipeline.step6Prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/train', methods=['GET'])
def training():
    os.system('python main.py')
    return 'Training successful'

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Fetching form data
            fixedAcidity = float(request.form['fixedAcidity'])
            volatileAcidity = float(request.form['volatileAcidity'])
            citricAcid = float(request.form['citricAcid'])
            residualSugar = float(request.form['residualSugar'])
            chlorides = float(request.form['chlorides'])
            freeSulfurDioxide = float(request.form['freeSulfurDioxide'])
            totalSulfurDioxide = float(request.form['totalSulfurDioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            # Prepare data for prediction
            data = [fixedAcidity, volatileAcidity, citricAcid, residualSugar, chlorides,
                    freeSulfurDioxide, totalSulfurDioxide, density, pH, sulphates, alcohol]
            data = np.array(data).reshape(1, 11)
            
            # Prediction
            obj = PredictionPipeline()
            pred = obj.predict(data)
            return render_template('results.html', prediction=str(pred))
        except Exception as e:
            return f'Something went wrong: {e}'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
