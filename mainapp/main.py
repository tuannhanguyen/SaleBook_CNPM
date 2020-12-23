from flask import render_template, request, redirect
from mainapp import app, utils
from mainapp.filters import *
from mainapp import login
from mainapp.models import User
from flask_login import login_user


@app.route("/")
def index():
    categories = ["ALL", "VĂN HỌC", "KINH TẾ", "SÁCH THIẾU NHI", "SÁCH NGOẠI NGỮ"]
    kw = request.args.get("keyword")
    if kw:
        result = []
        for cat in categories:
            if cat in categories(kw) >= 0:
                result.append(cat)
    else:
        result = categories
    return render_template('index.html', categories=result)


@app.route("/<int:id>")
def index2(id):
    if id == 1:
        return render_template('index.html', categories=["VĂN HỌC", "KINH TẾ"])
    else:
        return render_template('index.html', categories=["SÁCH THIẾU NHI", "SÁCH NGOẠI NGỮ"])


@app.route('/products')
def product_list():
    books = utils.read_book()
    return render_template('product-list.html', books=books)


@app.route('/product-economic')
def product_list_economic():
    books = utils.read_book()
    return render_template('product-economy.html', books=books)


@app.route('/product-literature')
def product_list_literature():
    books = utils.read_book()
    return render_template('product-literature.html', books=books)


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)  # select * from User where id = userid


@app.route('/login', methods=['get', 'post'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user:
            login_user(user=user)
    return redirect('/admin')  # neu method = get


if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True)
