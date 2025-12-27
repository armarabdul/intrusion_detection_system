import pandas as pd
import os

# NSL-KDD feature column names (41 features)
NSL_KDD_FEATURES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
    'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
    'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate'
]

def load_nsl_kdd_data(file_path):
    """Load NSL-KDD data file and return DataFrame with proper column names."""
    df = pd.read_csv(file_path, header=None, sep=',')
    
    # Assign column names: 41 features + label + optional attack_type
    column_names = NSL_KDD_FEATURES + ['label']
    if df.shape[1] == 43:
        column_names.append('attack_type')
    
    df.columns = column_names
    return df

def save_csv_files(train_df, test_df, output_dir='data/raw'):
    """Save training and test DataFrames as CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    
    train_output = os.path.join(output_dir, 'nsl_kdd_train.csv')
    test_output = os.path.join(output_dir, 'nsl_kdd_test.csv')
    
    train_df.to_csv(train_output, index=False)
    test_df.to_csv(test_output, index=False)
    
    print(f"Saved training data: {train_output}")
    print(f"Saved test data: {test_output}")

def get_normal_traffic(df):
    """Filter and return only rows where label == 'normal' for unsupervised training."""
    return df[df['label'] == 'normal'].copy()

if __name__ == '__main__':
    # Load training and test data
    train_file = 'data/raw/KDDTrain+.txt'
    test_file = 'data/raw/KDDTest+.txt'
    
    print("Loading training data...")
    train_df = load_nsl_kdd_data(train_file)
    print(f"Training data shape: {train_df.shape}")
    
    print("Loading test data...")
    test_df = load_nsl_kdd_data(test_file)
    print(f"Test data shape: {test_df.shape}")
    
    # Save as CSV files
    save_csv_files(train_df, test_df)
    
    # Demonstrate normal traffic filtering
    normal_train = get_normal_traffic(train_df)
    normal_test = get_normal_traffic(test_df)
    
    print(f"\nNormal traffic in training: {normal_train.shape[0]} rows")
    print(f"Normal traffic in test: {normal_test.shape[0]} rows")
    print(f"Attack rows in training: {train_df.shape[0] - normal_train.shape[0]} rows")
    print(f"Attack rows in test: {test_df.shape[0] - normal_test.shape[0]} rows")

