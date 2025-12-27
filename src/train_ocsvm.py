import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from src.preprocessing import get_normal_traffic

def get_numerical_features(df):
    """Extract behavior-centric numerical features, excluding label and attack_type."""
    exclude_cols = ['protocol_type', 'service', 'flag', 'label', 'attack_type']
    numerical_features = df.select_dtypes(include=[np.number]).columns.tolist()
    return [col for col in numerical_features if col not in exclude_cols]

def train_ocsvm(train_file='data/raw/nsl_kdd_train.csv',
                scaler_path='models/scaler.pkl',
                model_path='models/one_class_svm.pkl',
                nu=0.05,
                gamma='scale',
                kernel='rbf',
                random_state=42):
    """Train One-Class SVM model on normal traffic."""
    os.makedirs('models', exist_ok=True)
    
    print("Loading training data...")
    train_df = pd.read_csv(train_file)
    
    print("Filtering normal traffic...")
    normal_df = get_normal_traffic(train_df)
    print(f"Normal traffic samples: {normal_df.shape[0]}")
    
    print("Selecting numerical features...")
    feature_cols = get_numerical_features(normal_df)
    X_train = normal_df[feature_cols].values
    print(f"Feature dimensions: {X_train.shape}")
    
    print("Loading scaler...")
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
        print(f"Loaded existing scaler from {scaler_path}")
    else:
        print("Creating new scaler...")
        scaler = StandardScaler()
        scaler.fit(X_train)
        joblib.dump(scaler, scaler_path)
        print("Scaler saved")
    
    X_train_scaled = scaler.transform(X_train)
    
    print(f"Training One-Class SVM (kernel={kernel}, nu={nu})...")
    model = OneClassSVM(
        kernel=kernel,
        nu=nu,
        gamma=gamma
    )
    model.fit(X_train_scaled)
    
    print("Saving model...")
    joblib.dump(model, model_path)
    print("One-Class SVM model saved")
    
    print("Generating anomaly scores on training data...")
    anomaly_scores = model.decision_function(X_train_scaled)
    
    return model, scaler, anomaly_scores, feature_cols

def main():
    model, scaler, scores, features = train_ocsvm()
    print(f"\nAnomaly scores statistics:")
    print(f"Min: {scores.min():.4f}, Max: {scores.max():.4f}")
    print(f"Mean: {scores.mean():.4f}, Std: {scores.std():.4f}")

if __name__ == "__main__":
    main()

