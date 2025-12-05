# app/controllers/employees_controller.py

from flask import jsonify,request
from app.connections import get_db
from app.models.employees_model import Employee,EmployeeSalary,EmpCustRelation
from app.models.customers_model import Customer,CustomerAddress
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
from datetime import date
from sqlalchemy import and_,func


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
    - field:
        'salary_amount'  -> maps to base_salary
        'payment_method' -> enum
        'payment'        -> partial payment
        'currency'       -> 'USD' | 'LBP'
        'net_amount'     -> direct net_salary override (no recompute)
    """
    employee_username = data.get("employee_username")
    salary_month_str = data.get("salary_month")  # "YYYY-MM-01"
    field = data.get("field")
    value = data.get("value")

    # basic validation
    if not employee_username:
        return {"error": "employee_username is required"}, 400
    if not salary_month_str:
        return {"error": "salary_month is required"}, 400
    if not field:
        return {"error": "field is required"}, 400

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

        # ---- helper to safely cast to Decimal ----
        def d(val, default="0.00"):
            if val is None:
                return Decimal(default)
            if isinstance(val, Decimal):
                return val
            return Decimal(str(val))

        # ---- create if not exists ----
        if row is None:
            # default currency
            initial_currency = "LBP"
            if field == "currency":
                if value not in ("USD", "LBP"):
                    return {"error": "Invalid currency"}, 400
                initial_currency = value

            row = EmployeeSalary(
                employee_username=employee_username,
                salary_month=salary_month,
                base_salary=Decimal("0.00"),
                payment=Decimal("0.00"),
                bonus=Decimal("0.00"),
                deductions=Decimal("0.00"),
                net_salary=Decimal("0.00"),
                currency=initial_currency,
                payment_method="cash",
            )
            session.add(row)

        # ---- apply field update ----
        recalc_net = False  # only recompute net when relevant

        if field == "salary_amount":
            # update base_salary
            try:
                amount = Decimal(str(value))
            except Exception:
                return {"error": "salary_amount must be numeric"}, 400

            if amount < 0:
                return {"error": "salary_amount cannot be negative"}, 400

            row.base_salary = amount
            recalc_net = True

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
            recalc_net = True

        elif field == "currency":
            curr = (value or "").strip().upper()
            if curr not in ("USD", "LBP"):
                return {"error": "Invalid currency"}, 400
            row.currency = curr

        elif field == "net_amount":
            # direct override of net_salary, NO formula recompute
            try:
                net_val = Decimal(str(value))
            except Exception:
                return {"error": "net_amount must be numeric"}, 400

            row.net_salary = net_val
            # do NOT set recalc_net = True here

        else:
            return {"error": f"Unsupported field '{field}'"}, 400

        # ---- recompute net_salary ONLY when needed ----
        if recalc_net:
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
            "currency": row.currency,
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


def get_customers_not_in_emp_relation():
    db = get_db()
    s = db.get_session()

    try:
        # Subquery of ALL customer usernames that appear in the relation table
        subq = s.query(EmpCustRelation.cust_username).distinct().subquery()

        rows = (
            s.query(
                Customer.username,
                Customer.fullname,
                Customer.mobile,
                CustomerAddress.city.label("addr_city"),
                CustomerAddress.village.label("addr_village"),
                CustomerAddress.street.label("addr_street"),
                CustomerAddress.building.label("addr_building"),
                CustomerAddress.floor.label("addr_floor"),
            )
            .outerjoin(
                CustomerAddress,
                Customer.username == CustomerAddress.username,
            )
            # Customers whose username is NOT in relation table
            .filter(~Customer.username.in_(subq))
            .order_by(Customer.fullname)
            .all()
        )

        result = []
        for r in rows:
            # Build a single address string from available parts
            address_parts = [
                r.addr_city,
                r.addr_village,
                r.addr_street,
                r.addr_building,
                r.addr_floor,
            ]
            address = " ".join(
                str(p).strip() for p in address_parts if p is not None and str(p).strip()
            )

            result.append(
                {
                    "username": r.username,
                    "fullname": r.fullname,
                    "mobile": r.mobile,
                    "address": address,          # for filtering by first word
                    "customeraddress": address,  # alias if you want this name too
                }
            )

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()

def assign_customers_to_employee(emp_username: str, cust_usernames: list[str]):
    """
    Create EmpCustRelation rows for given employee and customer usernames.
    Returns (result_dict, status_code)
    """
    db = get_db()
    s = db.get_session()

    try:
        if not emp_username:
            return {"error": "emp_username is required"}, 400

        if not cust_usernames or not isinstance(cust_usernames, list):
            return {"error": "cust_usernames must be a non-empty list"}, 400

        # Fetch existing relations to avoid duplicates
        existing_rows = (
            s.query(EmpCustRelation.cust_username)
            .filter(
                EmpCustRelation.emp_username == emp_username,
                EmpCustRelation.cust_username.in_(cust_usernames),
            )
            .all()
        )
        existing = {row.cust_username for row in existing_rows}

        # Build new rows only for usernames not yet linked
        to_insert = [
            EmpCustRelation(emp_username=emp_username, cust_username=u)
            for u in cust_usernames
            if u not in existing
        ]

        if to_insert:
            s.add_all(to_insert)
            s.commit()

        return {
            "success": True,
            "emp_username": emp_username,
            "inserted_count": len(to_insert),
            "skipped_existing": list(existing),
        }, 200

    except SQLAlchemyError as e:
        s.rollback()
        return {"error": str(e)}, 500

    finally:
        s.close()

def load_customers_for_employee(emp_username: str):
    """
    Load customers already related to an employee via EmpCustRelation.

    Returns:
        (result: dict | list, status_code: int)
    """
    db = get_db()
    s = db.get_session()

    try:
        if not emp_username:
            return {"error": "emp_username is required"}, 400

        # join EmpCustRelation -> Customer -> CustomerAddress (optional)
        rows = (
            s.query(
                Customer.username,
                Customer.fullname,
                Customer.mobile,
                func.concat_ws(
                    " - ",
                    CustomerAddress.city,
                    CustomerAddress.village,
                    CustomerAddress.street,
                    CustomerAddress.building,
                    CustomerAddress.floor,
                ).label("customeraddress"),
            )
            .join(
                EmpCustRelation,
                EmpCustRelation.cust_username == Customer.username,
            )
            .outerjoin(
                CustomerAddress,
                CustomerAddress.username == Customer.username,
            )
            .filter(EmpCustRelation.emp_username == emp_username)
            .order_by(Customer.fullname)
            .all()
        )

        result = [
            {
                "username": r.username,
                "fullname": r.fullname,
                "mobile": r.mobile,
                "customeraddress": r.customeraddress or "",
            }
            for r in rows
        ]

        return result, 200

    except SQLAlchemyError as e:
        # if you want to log:
        # current_app.logger.exception("Error loading customers for employee")
        return {"error": str(e)}, 500

    finally:
        s.close()


def delete_customers_by_usernames(usernames: list):
    """
    Delete customers (and their addresses) completely from DB,
    given a list of usernames.
    """
    db = get_db()
    s = db.get_session()

    try:
      if not usernames:
          return {"success": True, "deleted_customers": 0}, 200

      # 1) delete addresses first (if FK)
      s.query(CustomerAddress).filter(
          CustomerAddress.username.in_(usernames)
      ).delete(synchronize_session=False)

      # 2) delete customer rows
      deleted = s.query(Customer).filter(
          Customer.username.in_(usernames)
      ).delete(synchronize_session=False)

      s.commit()

      return {"success": True, "deleted_customers": deleted}, 200

    except SQLAlchemyError as e:
        s.rollback()
        return {"error": str(e)}, 500

    finally:
        s.close()


def unassign_customers_controller():
    """Controller logic to unassign multiple customers from an employee."""

    db = get_db()
    s = db.get_session()

    try:
        data = request.get_json() or {}

        emp_username = data.get("emp_username")
        cust_usernames = data.get("cust_usernames") or []

        # Validate
        if not emp_username:
            return jsonify({"error": "emp_username is required"}), 400

        if not isinstance(cust_usernames, list) or len(cust_usernames) == 0:
            return jsonify({"error": "cust_usernames must be a non-empty list"}), 400

        # Clean usernames
        cust_usernames = [
            (u or "").strip()
            for u in cust_usernames
            if (u or "").strip()
        ]

        if not cust_usernames:
            return jsonify({"error": "cust_usernames list is empty after cleaning"}), 400

        # Delete relations
        deleted_count = (
            s.query(EmpCustRelation)
            .filter(
                EmpCustRelation.emp_username == emp_username,
                EmpCustRelation.cust_username.in_(cust_usernames),
            )
            .delete(synchronize_session=False)
        )

        s.commit()

        return jsonify({
            "message": "Customers unassigned successfully.",
            "emp_username": emp_username,
            "cust_usernames": cust_usernames,
            "deleted_rows": deleted_count,
        }), 200

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()