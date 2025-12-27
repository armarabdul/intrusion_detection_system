import os
import joblib
import numpy as np
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from api.models import db, DetectionResult
from api.rate_limit import rate_limit

inference_bp = Blueprint('inference', __name__)

MODELS = {}
SCALER = None
THRESHOLD = None
TRAINING_STATS = None
FEATURE_COLS = [
    'duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
    'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

FEATURE_NAMES = {
    'duration': 'Connection Duration',
    'src_bytes': 'Source Bytes',
    'dst_bytes': 'Destination Bytes',
    'count': 'Connection Count',
    'srv_count': 'Service Count',
    'serror_rate': 'SYN Error Rate',
    'rerror_rate': 'REJ Error Rate',
    'dst_host_count': 'Destination Host Count',
    'dst_host_srv_count': 'Destination Host Service Count',
    'num_failed_logins': 'Failed Login Attempts',
    'num_root': 'Root Access Attempts',
    'same_srv_rate': 'Same Service Rate'
}

def load_models(model_dir=None):
    global MODELS, SCALER, THRESHOLD, TRAINING_STATS
    if MODELS:
        return
    
    if model_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(base_dir, 'models')
    
    try:
        SCALER = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        MODELS['isolation_forest'] = joblib.load(os.path.join(model_dir, 'isolation_forest.pkl'))
        MODELS['ocsvm'] = joblib.load(os.path.join(model_dir, 'one_class_svm.pkl'))
        THRESHOLD = joblib.load(os.path.join(model_dir, 'threshold.pkl'))
        
        TRAINING_STATS = {
            'mean': SCALER.mean_ if hasattr(SCALER, 'mean_') else None,
            'std': SCALER.scale_ if hasattr(SCALER, 'scale_') else None
        }
        print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        raise

def get_risk_level(anomaly_score, threshold):
    if anomaly_score < threshold:
        return 'High'
    elif anomaly_score < threshold * 1.5:
        return 'Medium'
    else:
        return 'Low'

def calculate_confidence(anomaly_score, threshold):
    if anomaly_score < threshold:
        confidence = int(95 - ((threshold - anomaly_score) / threshold) * 15)
    elif anomaly_score < threshold * 1.5:
        confidence = int(85 - ((anomaly_score - threshold) / (threshold * 0.5)) * 15)
    else:
        confidence = int(70 - ((anomaly_score - threshold * 1.5) / (threshold * 2)) * 20)
    
    return max(50, min(95, confidence))

def check_data_drift(feature_values):
    if TRAINING_STATS is None or TRAINING_STATS['mean'] is None:
        return False
    
    try:
        feature_array = np.array([feature_values])
        scaled_features = SCALER.transform(feature_array)[0]
        mean_values = TRAINING_STATS['mean']
        std_values = TRAINING_STATS['std']
        
        z_scores = np.abs((scaled_features - mean_values) / (std_values + 1e-8))
        max_z_score = np.max(z_scores)
        
        return max_z_score > 3.0
    except:
        return False

def generate_explanation(feature_values, feature_names, scaled_features):
    try:
        if TRAINING_STATS is None or TRAINING_STATS['mean'] is None:
            return "Analysis completed based on ensemble model scoring."
        
        mean_values = TRAINING_STATS['mean']
        deviations = np.abs(scaled_features[0] - mean_values)
        
        top_indices = np.argsort(deviations)[-5:][::-1]
        
        explanations = []
        for idx in top_indices:
            if idx >= len(feature_names):
                continue
            feature_name = feature_names[idx]
            display_name = FEATURE_NAMES.get(feature_name, feature_name.replace('_', ' ').title())
            deviation = deviations[idx]
            
            if deviation > 2.0:
                explanations.append(f"{display_name} significantly deviates from normal patterns")
            elif deviation > 1.0:
                explanations.append(f"{display_name} shows unusual values")
        
        if explanations:
            return ". ".join(explanations[:3]) + "."
        return "Input shows moderate deviations from normal traffic patterns."
    except:
        return "Analysis completed based on ensemble model scoring."

@inference_bp.route('/detect', methods=['POST'])
@login_required
@rate_limit(max_requests=30, window_minutes=1)
def detect():
    if not MODELS or SCALER is None or THRESHOLD is None:
        try:
            load_models()
        except Exception as e:
            return jsonify({'error': 'Model loading failed'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        feature_values = []
        for col in FEATURE_COLS:
            if col not in data:
                return jsonify({'error': f'Missing feature: {col}'}), 400
            try:
                feature_values.append(float(data[col]))
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {col}'}), 400
        
        X = np.array([feature_values])
        X_scaled = SCALER.transform(X)
        
        if_scores = MODELS['isolation_forest'].decision_function(X_scaled)[0]
        ocsvm_scores = MODELS['ocsvm'].decision_function(X_scaled)[0]
        if_predictions = MODELS['isolation_forest'].predict(X_scaled)[0]
        ocsvm_predictions = MODELS['ocsvm'].predict(X_scaled)[0]
        
        ensemble_score = (if_scores + ocsvm_scores) / 2.0
        
        if_flagged = if_predictions == -1
        ocsvm_flagged = ocsvm_predictions == -1
        
        if if_flagged and ocsvm_flagged:
            agreement = 'Strong'
        elif if_flagged or ocsvm_flagged:
            agreement = 'Partial'
        else:
            agreement = 'None'
        
        risk_level = get_risk_level(ensemble_score, THRESHOLD)
        confidence = calculate_confidence(ensemble_score, THRESHOLD)
        
        drift_warning = check_data_drift(feature_values)
        explanation = generate_explanation(feature_values, FEATURE_COLS, X_scaled)
        
        result = DetectionResult(
            user_id=current_user.id,
            anomaly_score=float(ensemble_score),
            risk_level=risk_level,
            confidence=confidence,
            explanation=explanation,
            model_agreement=agreement,
            drift_warning=drift_warning
        )
        db.session.add(result)
        db.session.commit()
        
        from api.models import AuditLog
        audit_msg = f"Detection completed: {risk_level} risk (score: {ensemble_score:.4f}, confidence: {confidence}%)"
        audit = AuditLog(
            user_id=current_user.id,
            event_type='detection',
            message=audit_msg,
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        
        if risk_level == 'High':
            high_risk_audit = AuditLog(
                user_id=current_user.id,
                event_type='high_risk_detection',
                message=f"High-risk anomaly detected (score: {ensemble_score:.4f})",
                ip_address=request.remote_addr
            )
            db.session.add(high_risk_audit)
        
        db.session.commit()
        
        return jsonify({
            'anomaly_score': float(ensemble_score),
            'risk_level': str(risk_level),
            'confidence': float(confidence),
            'explanation': str(explanation),
            'model_agreement': str(agreement),
            'drift_warning': bool(drift_warning)
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
