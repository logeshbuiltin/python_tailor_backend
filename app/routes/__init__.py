from app.routes.auth_routes import auth_bp
from app.routes.category_routes import category_bp
from app.routes.item_routes import item_bp
from app.routes.image_routes import image_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(image_bp)
