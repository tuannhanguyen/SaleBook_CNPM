import os

from flask import render_template, request, session, redirect, jsonify, url_for
from mainapp import app, utils
from mainapp.filters import *
from mainapp import login
from mainapp.models import User
from flask_login import login_user, login_manager, current_user


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
    kw = request.args.get('kw')
    books = utils.read_book(kw=kw)
    return render_template('product-list.html', books=books)


@app.route("/products/<int:book_id>")
def product_detail(book_id):
    book = utils.get_book_by_id(book_id=book_id)

    return render_template('book-detail.html',
                           book=book)


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
    err = " "
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/login-user', methods=['get', 'post'])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password",'')

        user = utils.validate_user(username=username, password=password)
        if user:
            current_user.id = user.id
            return redirect(url_for("product_list"))
        else:
            err_msg = "Đăng nhập không thành công"

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            return redirect(url_for('admin_login'))
        else:
            err_msg = "Đăng nhập không thành công"

    return render_template('login.html', err_msg=err_msg)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            f = request.files["avatar"]
            avatar_path = 'images/upload/%s' % f.filename
            f.save(os.path.join(app.root_path, 'static/', avatar_path))
            if utils.register_user(name=name, username=username, password=password,
                                   email=email, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang bị lỗi! Vui lòng thực hiện sau!"
        else:
            err_msg = "Mật khâu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/cart', methods=['get', 'post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session['cart'] = cart

    total_quan, total_amount = utils.cart_starts(cart)
    # return jsonify({
    #     "total_amount": total_amount,
    #     "total_quantity": total_quan,
    #     "cart": cart
    # })
    return jsonify({
        "total_amount": total_amount,
        "total_quantity": total_quan
    })


@app.route('/pay')
def payment():
    total_quan, total_amount = utils.cart_starts(session.get('cart'))
    return render_template("payment.html", total_amount=total_amount, total_quan=total_quan)


@app.route('/api/pay', methods=['post'])
def pay():
    # if 'cart' in session and session['cart']:
    #     utils.add_receipt(cart=session['cart'])
    #     del session['cart']
    #
    #     return jsonify({'message': 'Đã thanh toán'})
    #
    # return jsonify({'message': 'failed'})
    if utils.add_receipt(session.get('cart')):
        del session['cart']

        return jsonify({
            "message": "Đã thanh toán",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })


@app.route('/api/cart/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 'cart' in session:
        cart = session['cart']
        if item_id in cart:
            del cart[item_id]
            session['cart'] = cart

            return jsonify({'err_msg': 'Thanh cong',
                            'code': 200,
                            'item_id': item_id
                            })

    return jsonify({'err_msg': 'that bai', 'code': 500})


@app.route('/api/cart/<item_id>', methods=['post'])
def update_item(item_id):
    if 'cart' in session:
        cart = session['cart']
        # du lieu gui len tu bo dy cua ham fetch
        data = request.json
        if item_id in cart and 'quantity' in data:
            cart[item_id]['quantity'] = int(data['quantity'])
            session['cart'] = cart
            total_quan, total_amount = utils.cart_starts(session.get('cart'))
            return jsonify({'err_msg': 'Thanh cong',
                            'code': 200,
                            'total_quantity': total_quan,
                            'total_amount': total_amount
                            })

        return jsonify({'err_msg': 'that bai', 'code': 500})


if __name__ == "__main__":
    from mainapp.admin_module import *

    app.run(debug=True)
