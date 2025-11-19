# app/routes/employees_routes.py

from flask import Blueprint, request,jsonify
from app.controllers.employees_controller import (
    save_employee_logic,
    get_employees_logic,
    inline_update_salary,
    get_employees_with_salary_logic,
)

employees_bp = Blueprint("employees_bp", __name__)


@employees_bp.post("/api/employees/saveemployee")
def save_employee_route():
    data = request.get_json() or {}
    return save_employee_logic(data)


@employees_bp.get("/api/employees")
def get_employees_route():
    return get_employees_logic()

@employees_bp.route("/api/employee-salaries/inline-update", methods=["POST"])
def api_inline_update_salary():
    data = request.get_json() or {}
    result, status = inline_update_salary(data)
    return jsonify(result), status

@employees_bp.get("/api/employees-with-salary")
def get_employees_with_salary_route():
    salary_month = request.args.get("salary_month")  # YYYY-MM-01
    return get_employees_with_salary_logic(salary_month)
