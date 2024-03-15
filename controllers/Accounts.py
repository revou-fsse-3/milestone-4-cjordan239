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
    user_id = request.form.get('user_id')
    account_type = request.form.get('account_type')
    account_number = request.form.get('account_number')

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    # Check if the user_id exists in the Users table
    user_exists = session.query(User).filter_by(user_id=user_id).first()
    if not user_exists:
        return jsonify({"error": "User ID does not exist"}), 400

    # Check if the user_id already has an account in the Accounts table
    existing_account = session.query(Account).filter_by(user_id=user_id).first()
    if existing_account:
        return jsonify({"error": "User already has an account"}), 400

    # If user_id exists and doesn't have an existing account, proceed to create the new account
    new_account = Account(user_id=user_id, account_type=account_type, account_number=account_number)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(new_account)
        session.commit()
        return jsonify({"message": "Account created successfully"}), 200
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Failed to create account"}), 500

@accounts_routes.route("/accounts/create", methods=['GET'])
def account_creation_success():
    return render_template("accounts/account_form.html")

# @accounts_routes.route("/accounts/create", methods=['GET'])
# def account_creation_success():
#     return render_template("account_success.html", message="Account created successfully")

