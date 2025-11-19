# app/controllers/employees_controller.py

from flask import jsonify
from app.connections import get_db
from app.models.employees_model import Employee,EmployeeSalary
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from datetime import date
from sqlalchemy import and_


def save_employee_logic(data):
    required = ["fullname", "mobile", "username", "city"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]

    if missing:
        return jsonify({
            "error": "Validation failed",
            "missing_fields": missing
        }), 400

    db = get_db()
    s = db.get_session()

    try:
        emp_id = data.get("id")

        if emp_id:
            # UPDATE
            employee = s.query(Employee).filter_by(id=emp_id).first()
            if not employee:
                return jsonify({"error": "Employee not found"}), 404
        else:
            # CREATE
            password_hash = (
                data.get("password_hash")
                or str(data.get("mobile", "")).strip()
                or "123456"
            )

            employee = Employee(
                fullname=data["fullname"].strip(),
                mobile=data["mobile"].strip(),
                username=data["username"].strip(),
                password_hash=password_hash
            )
            s.add(employee)

        # Common fields
        employee.fullname = data["fullname"].strip()
        employee.mobile = data["mobile"].strip()
        employee.username = data["username"].strip()

        employee.city = (data.get("city") or "").strip() or None
        employee.village = (data.get("village") or "").strip() or None
        employee.street = (data.get("street") or "").strip() or None
        employee.building = (data.get("building") or "").strip() or None
        employee.floor = (data.get("floor") or "").strip() or None

        emp_type = (data.get("type") or "").strip().lower()
        if emp_type:
            employee.type = emp_type
        elif not emp_id:
            employee.type = "home"

        s.commit()

        return jsonify({"status": "success", "id": employee.id}), \
               (201 if not emp_id else 200)

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()


def get_employees_logic():
    db = get_db()
    s = db.get_session()

    try:
        rows = (
            s.query(
                Employee.id,
                Employee.fullname,
                Employee.mobile,
                Employee.username,
                Employee.city,
                Employee.village,
                Employee.street,
                Employee.building,
                Employee.floor,
                Employee.type,
            )
            .order_by(Employee.id)
            .all()
        )

        result = [
            {
                "id": r.id,
                "fullname": r.fullname,
                "mobile": r.mobile,
                "username": r.username,
                "city": r.city or "",
                "village": r.village or "",
                "street": r.street or "",
                "building": r.building or "",
                "floor": r.floor or "",
                "type": r.type or "",
            }
            for r in rows
        ]

        return jsonify(result), 200

    finally:
        s.close()


def inline_update_salary(data: dict):
    """
    Handles inline update of EmployeeSalary:
    - Upserts by (employee_username, salary_month)
    - field: 'salary_amount' | 'payment_method' | 'payment'
    """
    employee_username = data.get("employee_username")
    salary_month_str = data.get("salary_month")  # "YYYY-MM-01"
    field = data.get("field")  # "salary_amount" | "payment_method" | "payment"
    value = data.get("value")

    # ---- basic payload validation ----
    if not employee_username or not salary_month_str or field not in (
        "salary_amount",
        "payment_method",
        "payment",
    ):
        return {"error": "Invalid payload"}, 400

    # parse date
    try:
        salary_month = date.fromisoformat(salary_month_str)
    except ValueError:
        return {"error": "Invalid salary_month format (expected YYYY-MM-DD)"}, 400
    
    db = get_db() 
    session = db.get_session()

    try:
        # find existing row for this employee + month
        row = (
            session.query(EmployeeSalary)
            .filter(
                and_(
                    EmployeeSalary.employee_username == employee_username,
                    EmployeeSalary.salary_month == salary_month,
                )
            )
            .one_or_none()
        )

        # create if not exists
        if row is None:
            row = EmployeeSalary(
                employee_username=employee_username,
                salary_month=salary_month,
                base_salary=Decimal("0.00"),
                payment=Decimal("0.00"),
                bonus=Decimal("0.00"),
                deductions=Decimal("0.00"),
                net_salary=Decimal("0.00"),
                currency="LBP",
                payment_method="cash",
            )
            session.add(row)

        # convenience: cast current values to Decimal safely
        def d(val, default="0.00"):
            if val is None:
                return Decimal(default)
            if isinstance(val, Decimal):
                return val
            return Decimal(str(val))

        # ---- apply field update ----
        if field == "salary_amount":
            # update base_salary
            try:
                amount = Decimal(str(value))
            except Exception:
                return {"error": "salary_amount must be numeric"}, 400

            if amount < 0:
                return {"error": "salary_amount cannot be negative"}, 400

            row.base_salary = amount

        elif field == "payment_method":
            pm = (value or "").strip().lower()
            allowed = {"cash", "card", "bank", "other"}
            if pm not in allowed:
                return {"error": "Invalid payment_method"}, 400
            row.payment_method = pm

        elif field == "payment":
            # numeric + bounds validation
            try:
                payment_amount = Decimal(str(value))
            except Exception:
                return {"error": "payment must be numeric"}, 400

            if payment_amount < 0:
                return {"error": "payment cannot be negative"}, 400

            base_salary = d(row.base_salary)
            # optional: prevent payment > base salary
            if base_salary > 0 and payment_amount > base_salary:
                return {
                    "error": "payment cannot be greater than base salary"
                }, 400

            row.payment = payment_amount

        # ---- recompute net_salary (example rule) ----
        # net = base + bonus - deductions - payment
        base = d(row.base_salary)
        bonus = d(row.bonus)
        deductions = d(row.deductions)
        payment_val = d(row.payment)

        row.net_salary = base + bonus - deductions - payment_val

        session.commit()

        return {
            "status": "ok",
            "base_salary": float(row.base_salary) if row.base_salary is not None else None,
            "payment": float(row.payment) if row.payment is not None else None,
            "net_salary": float(row.net_salary) if row.net_salary is not None else None,
            "payment_method": row.payment_method,
        }, 200

    except Exception as e:
        session.rollback()
        return {"error": str(e)}, 500

    finally:
        session.close()


def get_employees_logic():
    """
    Original function (unchanged). Returns employees only.
    """
    db = get_db()
    session = db.get_session()
    try:
        employees = session.query(Employee).order_by(Employee.id).all()

        return [
            {
                "id": e.id,
                "fullname": e.fullname,
                "mobile": e.mobile,
                "username": e.username,
                "city": e.city,
                "village": e.village,
                "street": e.street,
                "building": e.building,
                "floor": e.floor,
                "type": e.type,
            }
            for e in employees
        ]

    finally:
        session.close()



def get_employees_with_salary_logic(salary_month: str = None):
    """
    New function: returns employees + salary_amount + payment_method + net_salary
    for a specific month.
    Uses LEFT JOIN so employees always appear even with no salary record.
    """
    db = get_db()
    session = db.get_session()

    try:
        query = (
            session.query(
                Employee,
                EmployeeSalary.base_salary,
                EmployeeSalary.payment,
                EmployeeSalary.net_salary,
            )
            .outerjoin(
                EmployeeSalary,
                and_(
                    Employee.username == EmployeeSalary.employee_username,
                    EmployeeSalary.salary_month == salary_month
                    if salary_month
                    else True,
                ),
            )
            .order_by(Employee.fullname)
        )

        results = query.all()

        response = []
        for emp, base_salary, payment_method, net_salary in results:
            response.append(
                {
                    "id": emp.id,
                    "fullname": emp.fullname,
                    "mobile": emp.mobile,
                    "username": emp.username,
                    "city": emp.city,
                    "village": emp.village,
                    "street": emp.street,
                    "building": emp.building,
                    "floor": emp.floor,
                    "type": emp.type,
                    # salary fields
                    "salary_amount": float(base_salary) if base_salary else None,
                    "payment_method": payment_method,
                    "net_amount": float(net_salary) if net_salary else None,
                }
            )

        return response

    finally:
        session.close()


