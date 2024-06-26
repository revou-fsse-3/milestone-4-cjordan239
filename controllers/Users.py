from flask import Blueprint, render_template, request, jsonify, redirect
from connectors.mysql_connectors import Session
from models.Users import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, or_
from flask_login import current_user, login_required, login_user, logout_user
from connectors.mysql_connectors import engine

users_routes = Blueprint('users_routes', __name__)

@users_routes.route("/users", methods=['GET'])
def get_users():
    response_data = dict()
    session = Session()
    try:
        users_query = select(User)
        users = session.execute(users_query).scalars()
        response_data['users'] = [{'user_id': user.user_id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify(response_data), 200
    except Exception as e:
        return { "message": "Gagal dapat data" }


@users_routes.route("/users/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")    

@users_routes.route("/users/register", methods=['POST'])
def register_users():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    NewUser = User(username=username, email=email)
    NewUser.set_password(password)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(NewUser)
        session.commit()
        return redirect("/users/login")
    except Exception as e:
        session.rollback()
        return { "message": "Gagal Register" }
    

@users_routes.route("/users/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")
    
@users_routes.route("/users/login", methods=['POST'])
def login_func_user():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        user = session.query(User).filter(User.username==request.form['username']).first()

        if user == None:
            return {"message": "no username found"}
        
        if not user.check_password(request.form['password']):
            return {"message": 'password salah'}
        
        login_user(user, remember=False)
        return redirect("/users/landingpage")
    
    except Exception as e:
        print(e)
        return { "message": "Login Failed"}

@users_routes.route('/users/landingpage')
@login_required
def landingpage():
    return render_template('users/landingpage.html', username=current_user.username)

@users_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/users/login')



@users_routes.route("/users/landingpage/changepassword", methods=['GET', 'POST'])
@login_required
def update_profile():
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    session = Session()

    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        if user.check_password(request.form.get('old_password')):
            user.username = new_username
            user.set_password(new_password)

            session.commit()
            return redirect('/logout')
        else:
            return { "message": "Incorrect old password" }, 400

    except Exception as e:
        print(e)
        return { "message": "Failed to update profile" }, 500

@users_routes.route("/changepass", methods=['GET'])
def landing_page_profile():
    return render_template("users/profile.html", username=current_user.username)
    





        
