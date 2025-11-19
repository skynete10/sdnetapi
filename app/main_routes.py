from app.routes.users_route import users_bp
from app.routes.customers_route import customers_bp
from app.routes.employees_route import employees_bp
from app.routes.settings_routes import settings_bp

def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(settings_bp)

