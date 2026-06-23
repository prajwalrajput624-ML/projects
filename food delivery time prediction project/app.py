from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('best_model_xgb_pipeline.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = {
            'distance_km': float(request.form.get('distance_km')),
            'route_length_km': float(request.form.get('route_length_km')),
            'order_day': int(request.form.get('order_day')),
            'traffic_level': str(request.form.get('traffic_level')),
            'delivery_mode': str(request.form.get('delivery_mode')),
            'weather': str(request.form.get('weather_conditions')),
            'restaurant_zone': str(request.form.get('restaurant_zone')),
            'customer_zone': str(request.form.get('customer_zone'))
}

        
        data = pd.DataFrame([input_data])
        prediction = model.predict(data)
        
        result_text = f'Estimated Delivery Time: {prediction[0]:.2f} minutes'
        return render_template('index.html', prediction_text=result_text)

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
