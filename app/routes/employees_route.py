# app/routes/employees_routes.py

from flask import Blueprint, request,jsonify
from app.controllers.employees_controller import (
    save_employee_logic,
    get_employees_logic,
    inline_update_salary,
    get_employees_with_salary_logic,
    get_customers_not_in_emp_relation,
    assign_customers_to_employee,
    load_customers_for_employee,
    delete_customers_by_usernames,
    unassign_customers_controller,
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


@employees_bp.route("/api/employees/customers-not-in-relation", methods=["GET"])
def get_customers_not_in_emp_relation_route():
    return get_customers_not_in_emp_relation()


@employees_bp.post("/api/employees/assign-customers")
def assign_customers_to_employee_route():
    data = request.get_json(silent=True) or {}

    emp_username = data.get("emp_username")
    cust_usernames = data.get("cust_usernames") or []

    # make sure it's a list
    if isinstance(cust_usernames, str):
        cust_usernames = [cust_usernames]

    result, status_code = assign_customers_to_employee(
        emp_username=emp_username,
        cust_usernames=cust_usernames,
    )
    return jsonify(result), status_code

@employees_bp.get("/api/employees/customers-for-employee")
def load_customers_for_employee_route():
    emp_username = request.args.get("emp_username", type=str)

    result, status_code = load_customers_for_employee(emp_username)

    # result can be list (success) or dict (error), both jsonifiable
    return jsonify(result), status_code


@employees_bp.post("/api/employees/delete-customers")
def delete_customers_route():
    data = request.get_json() or {}
    cust_usernames = data.get("cust_usernames") or []

    result, status_code = delete_customers_by_usernames(cust_usernames)
    return jsonify(result), status_code


@employees_bp.post("/api/employees/unassign-customers")
def unassign_customers_route():
    return unassign_customers_controller()