import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score  
import joblib
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BLOOD_DEMAND_DATA_2020_FILE_PATH = BASE_DIR / 'data/blood_demand_data_2020.csv'
LINEAR_REGRESSION_MODEL_FILE_PATH = BASE_DIR / "data/linear_regression_model.joblib"
LABEL_ENCODER_FILE_PATH = BASE_DIR / "data/label_encoder.joblib"



def train_random_forest_regressor_model(data):
    # Drop unnecessary columns
    features = data.drop(columns=["Blood Demand", "Date" ])
    label_encoder = LabelEncoder()

    # Convert Blood Type to numeric using one-hot encoding
    features["Blood Type"] = label_encoder.fit_transform(features["Blood Type"])
    features['Gender'] =  label_encoder.fit_transform(features["Gender"])

    # Create the X and y arrays
    X = features
    y = data["Blood Demand"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)


    # Initialize the Random Forest model
    rf_model = RandomForestRegressor(random_state=42)

    # Train the model
    rf_model.fit(X_train, y_train)


    # Save the trained model to a file so we can use it in other programs

    label_encoder.fit(data["Blood Type"])
    joblib.dump(rf_model, os.path.join(BASE_DIR, LINEAR_REGRESSION_MODEL_FILE_PATH))
    joblib.dump(label_encoder, os.path.join(BASE_DIR, LABEL_ENCODER_FILE_PATH))

    # calculate the mean squared error with testing dataset
    yy_pred = rf_model.predict(X_test)
    mse = mean_squared_error(y_test, yy_pred)
    print(f"Mean Squared Error (MSE): {mse}")

    # calculate accuracy in percentage
    accuracy = rf_model.score(X_test, y_test) * 100
    print(f"Accuracy: {round(accuracy, 2)}%")

    return rf_model, label_encoder


def predict_blood_demand(blood_type, temperature, age, gender, population, events):
     # Load the dataset from the CSV file
    data = pd.read_csv(BLOOD_DEMAND_DATA_2020_FILE_PATH)

    try:
        label_encoder = joblib.load(os.path.join(BASE_DIR, LABEL_ENCODER_FILE_PATH))
        model = joblib.load(os.path.join(BASE_DIR, LINEAR_REGRESSION_MODEL_FILE_PATH))
    except FileNotFoundError:
        # attempt to load the model and label encoder
        print("Model and label encoder not found. Training the model...")
        model, label_encoder = train_random_forest_regressor_model(data)
    
    # Convert Gender to numeric using one-hot encoding
    print("GENDER :: ", gender)
    if gender.lower() == 'male':
        gender = 1
    else:
        gender = 0


    data_params = pd.DataFrame({
        "Temperature (°C)": [temperature],
        "Blood Type": label_encoder.transform([blood_type]),
        "Age": [age],
        "Gender": gender,
        'Population': [population],
        "Events": [events],
    })
    y_pred = model.predict(data_params)

    return y_pred


if __name__ == "__main__":
    result = predict_blood_demand(blood_type="A+", temperature=30, age=60, gender="Male", population=100000, events=0)
    print(result)