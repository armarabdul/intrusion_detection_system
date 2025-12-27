import numpy as np
import joblib
import os

def compute_threshold(anomaly_scores, percentile=95):
    """Compute anomaly threshold using percentile-based logic."""
    threshold = np.percentile(anomaly_scores, percentile)
    return threshold

def save_threshold(threshold, threshold_path='models/threshold.pkl'):
    """Save computed threshold to file."""
    os.makedirs('models', exist_ok=True)
    joblib.dump(threshold, threshold_path)
    print("Threshold saved")

def compute_and_save_threshold(anomaly_scores, percentile=95, threshold_path='models/threshold.pkl'):
    """Compute threshold from anomaly scores and save it."""
    threshold = compute_threshold(anomaly_scores, percentile)
    save_threshold(threshold, threshold_path)
    return threshold

def main():
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from src.train_isolation_forest import train_isolation_forest
    
    print("Training Isolation Forest to generate anomaly scores...")
    _, _, scores, _ = train_isolation_forest()
    
    print(f"\nComputing threshold at 95th percentile...")
    threshold = compute_and_save_threshold(scores, percentile=95)
    print(f"Threshold value: {threshold:.4f}")
    print(f"Scores below threshold: {(scores < threshold).sum()} / {len(scores)}")

if __name__ == "__main__":
    main()

