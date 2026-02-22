import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

priority_model = joblib.load(os.path.join(BASE_DIR, "models/priority_xgb.pkl"))
resolution_model = joblib.load(os.path.join(BASE_DIR, "models/resolution_xgb.pkl"))
forecast_model = joblib.load(os.path.join(BASE_DIR, "models/forecast_xgb.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "models/priority_label_encoder.pkl"))

priority_columns = joblib.load(os.path.join(BASE_DIR, "models/priority_feature_columns.pkl"))
resolution_columns = joblib.load(os.path.join(BASE_DIR, "models/resolution_feature_columns.pkl"))
forecast_columns = joblib.load(os.path.join(BASE_DIR, "models/forecast_feature_columns.pkl"))

def preprocess_input(data_dict):
    df = pd.DataFrame([data_dict])
    df = pd.get_dummies(df)

    # Ensure columns match training model
    model_columns = priority_model.get_booster().feature_names

    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[model_columns]
    return df


def predict_priority(data_dict):
    df = preprocess_input(data_dict)
    pred = priority_model.predict(df)
    return label_encoder.inverse_transform(pred)[0]


def predict_resolution(data_dict):
    df = preprocess_input(data_dict)
    return round(resolution_model.predict(df)[0], 1)
