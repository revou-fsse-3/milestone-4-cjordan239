from flask import Blueprint, render_template, request, jsonify, redirect
from connectors.mysql_connectors import Session
from models.Accounts import Account
from models.Users import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, or_
from flask_login import current_user, login_required, login_user, logout_user
from connectors.mysql_connectors import engine


accounts_routes = Blueprint('accounts_routes', __name__)

@accounts_routes.route("/accounts/create", methods=['POST'])
@login_required
def create_account():
    try:
        account_type = request.form['account_type']  # Use square brackets [] instead of ()
        account_number = request.form['account_number']  # Use square brackets [] instead of ()

        new_account = Account(
            user_id=current_user.user_id,
            account_type=account_type,
            account_number=account_number
        )

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        session.add(new_account)
        session.commit()

        return jsonify({"message": "Account created successfully!"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@accounts_routes.route("/accounts/create", methods=['GET'])
def account_creation_success():
    return render_template("accounts/account_form.html")


# @accounts_routes.route("/accounts/create", methods=['GET'])
# def account_creation_success():
#     return render_template("account_success.html", message="Account created successfully")

