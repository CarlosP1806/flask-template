from flask import Flask, jsonify
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .services import db_service 
    db_service.init_app(app)

    from .blueprints import songs
    app.register_blueprint(songs.bp)

    @app.route('/healthz')
    def health():
        return jsonify({'status': 'ok'})
    
    @app.route("/test")
    def test():
        return jsonify({"message": "Hello, World!"})
    
    return app
