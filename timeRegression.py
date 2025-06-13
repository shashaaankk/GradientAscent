import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

SCALER_PATH = os.path.join("data", "scaler.pkl")

def load_and_preprocess_data(csv_path):
    df = pd.read_csv(csv_path)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df.drop(columns=['duration']))
    df_scaled = pd.DataFrame(X_scaled, columns=df.columns[:-1])
    df_scaled['duration'] = df['duration']
    
    # Save the scaler
    joblib.dump(scaler, SCALER_PATH)
    
    return df_scaled, scaler

def load_scaler(path=SCALER_PATH):
    return joblib.load(path)

def split_data(df_scaled, test_size=0.2):
    X = df_scaled.drop(columns=['duration'])
    y = df_scaled['duration']
    return train_test_split(X, y, test_size=test_size, random_state=42)

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n🔎 Model Evaluation:")
    print(f"Mean Absolute Error: {mae / 60:.2f} minutes")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {mse**0.5}")
    print(f"Mean Absolute Percentage Error: {mae / y_test.mean() * 100:.2f}%")
    print(f"R^2 Score: {r2:.4f}")
    return y_pred

def compare_predictions(model, X_train, y_train, n=10):
    sample = X_train.sample(n=n, random_state=1)
    actual = y_train.loc[sample.index]
    predicted = model.predict(sample)
    comparison = pd.DataFrame({
        'Actual Duration (min)': actual.values,
        'Predicted Duration (min)': predicted,
        'Error (min)': predicted - actual.values
    }, index=sample.index)
    print("\n🎯 Sample Prediction Comparison:")
    print(comparison.round(2))

def plot_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        plt.figure(figsize=(8, 4))
        plt.barh(feature_names, importances)
        plt.xlabel("Importance")
        plt.title("🌲 Feature Importance (Random Forest)")
        plt.tight_layout()
        plt.show()

def plot_residuals(y_test, y_pred):
    residuals = y_test - y_pred
    sns.histplot(residuals, kde=True)
    plt.title("📉 Residual Distribution")
    plt.xlabel("Residual (Actual - Predicted)")
    plt.tight_layout()
    plt.show()

def get_user_input():
    """
    Replace this with actual user input or a GUI/CLI.
    Input must be a dict with keys matching the feature names.
    """
    return {
        "feature1": 0.5,
        "feature2": 0.8,
        "feature3": 0.3,
        # ...
    }

def predict_from_input(model, user_input_dict):
    # Load scaler and ensure input format
    scaler = load_scaler()
    input_df = pd.DataFrame([user_input_dict])
    input_scaled = scaler.transform(input_df)
    
    # Predict
    prediction = model.predict(input_scaled)[0]
    print(f"\n⏱️ Predicted Duration: {prediction:.2f} minutes")
    return prediction

def main():
    base_csv = os.path.join("data", "output.csv")
    df_scaled, _ = load_and_preprocess_data(base_csv)
    X_train, X_test, y_train, y_test = split_data(df_scaled)

    model = RandomForestRegressor()
    print("📊 Training the model...")
    model = train_model(model, X_train, y_train)

    y_pred = evaluate_model(model, X_test, y_test)
    compare_predictions(model, X_train, y_train)
    # plot_feature_importance(model, X_train.columns)
    # plot_residuals(y_test, y_pred)

    # Predict from user input
    # user_input = get_user_input()
    # predict_from_input(model, user_input)

if __name__ == "__main__":
    main()
