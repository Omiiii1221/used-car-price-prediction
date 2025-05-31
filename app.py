from flask import Flask, request, render_template
import numpy as np
import joblib
from datetime import datetime

app = Flask(__name__)

# Load the trained model and scalers
model = joblib.load('rf_model.joblib')
scaler_X = joblib.load('scaler_X.joblib')
scaler_y = joblib.load('scaler_y.joblib')

MODEL_NAME_MAP = {
    0: "Alto", 1: "Baleno", 2: "City", 3: "Creta", 4: "Duster", 5: "EcoSport",
    6: "Elite", 7: "Grand", 8: "i10", 9: "i20", 10: "Innova", 11: "Jazz",
    12: "Nexon", 13: "Octavia", 14: "Polo", 15: "Swift", 16: "Verna", 17: "Wagon"
    # Update this mapping to match your actual label encoding!
}

TRANSMISSION_MAP = {0: "Automatic", 1: "Manual"}
FUEL_TYPE_MAP = {0: "CNG", 1: "Diesel", 2: "Petrol"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model_name = int(request.form['model_name'])
        manufacturing_year = int(request.form['manufacturing_year'])
        engine_capacity = int(request.form['engine_capacity'])
        transmission = int(request.form['transmission'])
        km_driven = int(request.form['km_driven'])
        ownership = int(request.form['ownership'])
        fuel_type = int(request.form['fuel_type'])
        imperfections = int(request.form['imperfections'])
        repainted_parts = int(request.form['repainted_parts'])

        input_features = np.array([[model_name, manufacturing_year, engine_capacity,
                                    transmission, km_driven,
                                    ownership, fuel_type, imperfections, repainted_parts]])

        input_features_scaled = scaler_X.transform(input_features)
        prediction_scaled = model.predict(input_features_scaled)[0]
        prediction = scaler_y.inverse_transform([[prediction_scaled]])[0][0]

        # Prepare a dictionary of parsed values
        parsed_values = {
            "Model Name": MODEL_NAME_MAP.get(model_name, model_name),
            "Manufacturing Year": manufacturing_year,
            "Engine Capacity": engine_capacity,
            "Transmission": TRANSMISSION_MAP.get(transmission, transmission),
            "KM Driven": km_driven,
            "Ownership": ownership,
            "Fuel Type": FUEL_TYPE_MAP.get(fuel_type, fuel_type),
            "Imperfections": imperfections,
            "Repainted Parts": repainted_parts
        }

        return render_template(
            'index.html',
            prediction_text=f'Estimated Price: ₹ {round(prediction, 0)}',
            parsed_values=parsed_values
        )

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
