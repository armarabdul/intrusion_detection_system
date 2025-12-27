from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from api.models import db, DetectionResult, AuditLog

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    recent_results = DetectionResult.query.filter_by(user_id=current_user.id)\
        .order_by(DetectionResult.created_at.desc())\
        .limit(50)\
        .all()
    
    recent_logs = AuditLog.query.filter_by(user_id=current_user.id)\
        .order_by(AuditLog.created_at.desc())\
        .limit(20)\
        .all()
    
    return render_template('dashboard.html', user=current_user, results=recent_results, audit_logs=recent_logs)

@main_bp.route('/api/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = DetectionResult.query.filter_by(user_id=current_user.id)\
        .order_by(DetectionResult.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    results = [{
        'id': r.id,
        'anomaly_score': r.anomaly_score,
        'risk_level': r.risk_level,
        'created_at': r.created_at.isoformat()
    } for r in pagination.items]
    
    return jsonify({
        'results': results,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

