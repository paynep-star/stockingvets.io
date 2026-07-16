from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    from routes.auth import auth_bp
    from routes.portfolio import portfolio_bp
    from routes.verification import verification_bp
    from routes.forum import forum_bp
    from routes.stocks import stocks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    app.register_blueprint(verification_bp, url_prefix='/api/verification')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(stocks_bp, url_prefix='/api/stocks')
    
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, port=5000)