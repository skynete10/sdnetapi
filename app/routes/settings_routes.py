from flask import Blueprint
from app.controllers.settings_controller import (
    get_currency_settings,
    save_currency_settings
)

settings_bp = Blueprint("settings_bp", __name__)

settings_bp.route("/api/settings/currency", methods=["GET"])(
    get_currency_settings
)
settings_bp.route("/api/settings/currency", methods=["POST"])(
    save_currency_settings
)
