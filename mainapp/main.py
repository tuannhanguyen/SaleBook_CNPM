import os

import paypalrestsdk as paypalrestsdk
from flask import render_template, request, session, redirect, jsonify, url_for
from mainapp import app
from mainapp.filters import *
from mainapp import login
from flask_login import login_user, login_manager, current_user, logout_user, login_required


@app.route("/")
def index():
    return render_template('index.html')


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


@app.route('/product-science')
def product_list_science():
    books = utils.read_book()
    return render_template('product-science.html', books=books)


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
                                 password=password, role=UserRole.ADMIN)
        if user:
            login_user(user=user)

        user = utils.check_login(username=username,
                                 password=password, role=UserRole.USER)
        if user:
            login_user(user=user)
            return redirect('/')

    return redirect('/admin')


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
                err_msg = "Lỗi hệ thống"
        else:
            err_msg = "Mật khẩu không khớp"

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
        # du lieu gui len tu body cua ham fetch
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


@app.route("/login")
@login_required
def logout():
    logout_user()
    return redirect('/admin')


@app.route('/paypal')
def paypal():
    return render_template('paypal.html')


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "CLIENT_ID",
  "client_secret": "CLIENT_SECRET" })


@app.route('/payment', methods=['POST'])
def payment_():

    payment_ = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})


if __name__ == "__main__":
    from mainapp.admin_module import *

    app.run(debug=True)
