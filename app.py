from flask import Flask, render_template, Response, jsonify, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, RegisterForm
from flask_login import LoginManager, login_required, login_user, logout_user
from models import db, UserModel, Role, find_or_create_role
from lib.binomix import main
from werkzeug.utils import secure_filename
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:examplepassword@127.0.0.1/genesis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

db.init_app(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


@app.route("/")
def index():
    form_register = RegisterForm()
    form_login = LoginForm()
    return render_template('index.html', reg=form_register, login=form_login)


@app.route("/api/v<version>/login", methods=["POST"])
def login(version=1):
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                print(login_user(user, remember=form.remember_me.data))
                return redirect(url_for('panel'))
            else:
                return jsonify({'version': version, 'code': 404, 'error': True, 'message': 'Неправильный email или пароль'})
        else:
            return jsonify({'version': version, 'code': 404, 'error': True, 'message': 'Пользователя с таким email не зарегистрирован'})
    else:
        jsonify({'version': version, 'code': 422,
                'error': True, 'message': 'Некорректная форма'})
    return Response(status=200)


@app.route("/api/v<version>/register", methods=["POST"])
def register(version=1):
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if not user:
            try:
                hashed_password = generate_password_hash(form.password.data)
                user = UserModel(email=form.email.data,
                                 password=hashed_password)

                role = Role.query.filter_by(name='User').first()
                user.roles.append(role)

                db.session.execute(db.select())
                db.session.add(user)
                db.session.commit()
                return jsonify({'version': version, 'code': 200, 'error': False, 'message': 'Успешная регистрация'})
            except Exception as exp:
                db.session.rollback()
                print(exp)
                print("Ошибка добавления записи в БД!")
        else:
            return jsonify({'version': version, 'code': 409, 'error': True, 'message': 'Пользователь с таким email уже зарегистрирован'})
    return Response(status=200)


@app.route("/upload-file", methods=["POST"])
@login_required
def upload_file():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/panel", methods=["POST", "GET"])
@login_required
def panel():
    return render_template('panel.html')


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        find_or_create_role('Admin')
        find_or_create_role('User')
    app.run(host="0.0.0.0", port=3100, debug=True)
