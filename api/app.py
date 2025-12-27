from flask import Flask
from flask_login import LoginManager
from api.config import Config
from api.models import db, User
from api.auth import auth_bp
from api.routes import main_bp
from api.inference import inference_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../dashboard/templates', static_folder='../dashboard/static')
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(inference_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
        try:
            from api.inference import load_models
            model_dir = app.config.get('MODEL_DIR')
            load_models(model_dir)
        except Exception as e:
            print(f"Warning: Could not load models at startup: {e}")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

