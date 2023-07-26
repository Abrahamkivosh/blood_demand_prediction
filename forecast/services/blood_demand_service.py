import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score  #-0.001  0.0
import joblib
from pathlib import Path
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BLOOD_DEMAND_DATA_2020_FILE_PATH = BASE_DIR / 'data/blood_demand_data_2020.csv'
LINEAR_REGRESSION_MODEL_FILE_PATH = BASE_DIR / "data/linear_regression_model.joblib"
LABEL_ENCODER_FILE_PATH = BASE_DIR / "data/label_encoder.joblib"

def train_linear_regression_model(data):
    # Drop the 'Date' and 'Historical Blood Supply' columns as they are not required for Linear Regression
    data = data.drop(columns=['Date', 'Historical Blood Supply'])

    # Convert the 'Blood Type' column to numerical values using LabelEncoder
    le = LabelEncoder()
    data['Blood Type'] = le.fit_transform(data['Blood Type'])

    # Split the data into features (X) and target (y)
    X = data.drop(columns=['Blood Demand'])
    y = data['Blood Demand']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model to a file using joblib
    joblib.dump(model, LINEAR_REGRESSION_MODEL_FILE_PATH)
    joblib.dump(le, LABEL_ENCODER_FILE_PATH)  # Save the label encoder for blood type

    return model, le

def  processPrediction(model, label_encoder, temperature, blood_type):
    # Convert the blood type to numerical value using the label encoder
    blood_type_encoded = label_encoder.transform([blood_type])[0]

    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'Temperature (°C)': [temperature],
        'Blood Type': [blood_type_encoded]
    })

    # Make predictions on the input data
    y_pred = model.predict(input_data)
    return y_pred[0]
   

def predict_blood_demand(blood_type, temperature):
    # Load the dataset from the CSV file
    data = pd.read_csv(BLOOD_DEMAND_DATA_2020_FILE_PATH)

    try:
        # Attempt to load the trained model and label encoder from disk
        model = joblib.load(LINEAR_REGRESSION_MODEL_FILE_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_FILE_PATH)
    except FileNotFoundError:
        # Train the Linear Regression model if the saved files are not found
        print("Model and label encoder not found. Training the model...")
        model, label_encoder = train_linear_regression_model(data)

    response = processPrediction(model, label_encoder, temperature, blood_type)
    return response

    
