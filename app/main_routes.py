from app.routes.users_route import users_bp
from app.routes.customers_route import customers_bp
from app.routes.employees_route import employees_bp
from app.routes.settings_routes import settings_bp
from app.routes.services_routes import services_bp
from app.routes.customer_subscriptions_routes import customer_subscriptions_bp
from app.routes.internet_manager_routes import internet_manager_bp
from app.controllers.internet_manager_invoices_controller import bp as internet_manager_invoices_bp



def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(customer_subscriptions_bp)
    app.register_blueprint(internet_manager_bp)
    app.register_blueprint(internet_manager_invoices_bp)

