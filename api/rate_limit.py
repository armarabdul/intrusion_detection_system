from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict

rate_limit_store = defaultdict(list)

def rate_limit(max_requests=10, window_minutes=1):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"{request.remote_addr}"
            now = datetime.now()
            window_start = now - timedelta(minutes=window_minutes)
            
            requests = [req_time for req_time in rate_limit_store[key] if req_time > window_start]
            
            if len(requests) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
            
            requests.append(now)
            rate_limit_store[key] = requests
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

