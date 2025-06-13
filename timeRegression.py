import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
# from xgboost import XGBRegressor
# from sklearn.linear_model import Ridge

SCALER_PATH = os.path.join("data", "scaler.pkl")

def load_and_preprocess_data(csv_path):
    df = pd.read_csv(csv_path)
    feature_cols = [col for col in df.columns if col not in ['duration', 'break_time']]
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    df_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    df_scaled['time'] = df['duration'] #+ df['break_time']  # Assuming 'duration' and 'break_time' are present
    
    # Save the scaler
    joblib.dump(scaler, SCALER_PATH)
    
    return df_scaled, scaler

def load_scaler(path=SCALER_PATH):
    return joblib.load(path)

def split_data(df_scaled, test_size=0.2):
    X = df_scaled.drop(columns=['time'])
    y = df_scaled['time']
    return train_test_split(X, y, test_size=test_size, random_state=42)

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\nModel Evaluation:")
    print(f"Mean Absolute Error: {mae :.2f} seconds")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {mse**0.5}")
    print(f"Mean Absolute Percentage Error: {mae / y_test.mean() * 100:.2f}%")
    print(f"R^2 Score: {r2:.4f}")
    return y_pred

def compare_predictions(model, X_train, y_train, n=100):
    sample = X_train.sample(n=n, random_state=1)
    actual = y_train.loc[sample.index]
    predicted = model.predict(sample)
    comparison = pd.DataFrame({
        'Actual Duration (hr)': actual.values/3600,
        'Predicted Duration (hr)': predicted/3600,
        'Error (%)': abs(predicted - actual.values)/actual.values * 100
    }, index=sample.index)
    print("\nSample Prediction Comparison:")
    print(comparison.round(2))
    # print average error
    avg_error = comparison['Error (%)'].mean()
    print(f"\nAverage Error: {avg_error:.2f}%")

def plot_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        plt.figure(figsize=(8, 4))
        plt.barh(feature_names, importances)
        plt.xlabel("Importance")
        plt.title("Feature Importance (Random Forest)")
        plt.tight_layout()
        plt.show()

def plot_residuals(y_test, y_pred):
    residuals = y_test - y_pred
    sns.histplot(residuals, kde=True)
    plt.title("Residual Distribution")
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
    print(f"\nPredicted Duration: {prediction:.2f} minutes")
    return prediction

def main():
    base_csv = os.path.join("data", "output.csv")
    df_scaled, _ = load_and_preprocess_data(base_csv)
    X_train, X_test, y_train, y_test = split_data(df_scaled)

    model = RandomForestRegressor(
        n_estimators=200,        # More trees = better averaging
        max_depth=15,            # Limit tree depth to reduce overfitting
        min_samples_split=5,     # Require more samples to split nodes
        min_samples_leaf=2,      # Minimum number of samples in leaf nodes
        max_features='sqrt',     # Use sqrt(n_features) for each split (common best practice)
        bootstrap=True,          # Bootstrapping for better generalization
        random_state=42,
        n_jobs=-1                # Use all CPU cores
    )
    # model = XGBRegressor(
    #     n_estimators=300,        # More trees for better performance
    #     learning_rate=0.05,      # Smaller learning rate for smoother convergence
    #     max_depth=5,             # Depth 5 is often a sweet spot
    #     subsample=0.8,           # Prevent overfitting by sampling 80% of training data per tree
    #     colsample_bytree=0.8,    # Use 80% of features per tree
    #     gamma=0.1,               # Minimum loss reduction required to make a split (regularization)
    #     reg_alpha=0.1,           # L1 regularization term on weights
    #     reg_lambda=1.0,          # L2 regularization term on weights
    #     random_state=42,
    #     n_jobs=-1                # Use all available cores
    # )
    # model = Ridge(alpha=1.0)  # Regularization to prevent overfitting
    print("📊 Training the model...")
    model = train_model(model, X_train, y_train)

    y_pred = evaluate_model(model, X_test, y_test)
    compare_predictions(model, X_train, y_train)
    plot_feature_importance(model, X_train.columns)
    plot_residuals(y_test, y_pred)

    # Predict from user input
    # user_input = get_user_input()
    # predict_from_input(model, user_input)

if __name__ == "__main__":
    main()
