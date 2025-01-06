from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained RFC model
with open('best_rfc.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the expected feature names for the model
model_features = [
    'Sex', 'Age', 'Height', 'Overweight_Obese_Family',
    'Consumption_of_Fast_Food', 'Frequency_of_Consuming_Vegetables',
    'Number_of_Main_Meals_Daily', 'Food_Intake_Between_Meals', 'Smoking',
    'Liquid_Intake_Daily', 'Calculation_of_Calorie_Intake',
    'Physical_Excercise', 'Schedule_Dedicated_to_Technology',
    'Type_of_Transportation_Used'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect input data from the form
        input_data = {
            "Sex": request.form['Sex'],
            "Age": float(request.form['Age']),
            "Height": float(request.form['Height']),
            "Overweight_Obese_Family": int(request.form['Overweight_Obese_Family']),
            "Consumption_of_Fast_Food": int(request.form['Consumption_of_Fast_Food']),
            "Frequency_of_Consuming_Vegetables": int(request.form['Frequency_of_Consuming_Vegetables']),
            "Number_of_Main_Meals_Daily": int(request.form['Number_of_Main_Meals_Daily']),
            "Food_Intake_Between_Meals": int(request.form['Food_Intake_Between_Meals']),
            "Smoking": int(request.form['Smoking']),
            "Liquid_Intake_Daily": float(request.form['Liquid_Intake_Daily']),
            "Calculation_of_Calorie_Intake": int(request.form['Calculation_of_Calorie_Intake']),
            "Physical_Excercise": int(request.form['Physical_Excercise']),
            "Schedule_Dedicated_to_Technology": float(request.form['Schedule_Dedicated_to_Technology']),
            "Type_of_Transportation_Used": request.form['Type_of_Transportation_Used']
        }

        # Map categorical inputs
        input_data['Sex'] = 1 if input_data['Sex'].lower() == 'female' else 0
        input_data['Type_of_Transportation_Used'] = 1 if input_data['Type_of_Transportation_Used'].lower() == 'active' else 0

        # Convert input data into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Ensure all model features are present
        input_df = input_df.reindex(columns=model_features, fill_value=0)

        # Predict using the trained model
        prediction = model.predict(input_df)

        # Define categories for output (the prediction values will correspond to these)
        categories = {1: "Underweight", 2: "Normal", 3: "Overweight", 4: "Obesity"}

        # Ensure that the prediction is an integer (e.g., if it's an array or scalar)
        prediction_value = int(prediction[0]) if isinstance(prediction, (list, np.ndarray)) else int(prediction)

        # Map the numerical prediction to a readable category
        prediction_category = categories.get(prediction_value, "Unknown")

        # Return prediction result in a webpage
        return render_template('index.html', prediction=prediction_category)

    except Exception as e:
        # Handle errors and pass the error message to the template
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)


