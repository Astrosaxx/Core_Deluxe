from flask import Flask
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.secret_key = "n4jrUBrShSLPV_6ClB5tqQ"

    @app.template_filter('format_date')
    def format_date(date_str):
        if isinstance(date_str, str):
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return date_str
        else:
            date_obj = date_str
            
        return date_obj.strftime('%d/%m/%Y')
    from app.controllers.usuario_controller import bp as usuario_bp
    app.register_blueprint(usuario_bp)
    
    
    return app