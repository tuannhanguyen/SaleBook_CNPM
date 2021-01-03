import hashlib

from flask import session

from mainapp.models import Book, ReceiptDetail, Receipt, User, UserRole
from mainapp import db
from flask_login import current_user


def read_book(kw=None):
    books = Book.query
    if kw:
        books = books.filter(Book.name.contains(kw))
    return books.all()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def cart_starts(cart):
    count, price = 0, 0
    if cart:
        for p in cart.values():
            count = count + p["quantity"]
            price = price + p["price"] * p["quantity"]
    return count, price


def check_login(username, password, role):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user


def validate_user(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    user = User.query.filter(User.username == username, User.password == password,
                             User.user_role == UserRole.USER).first()

    return user


def register_user(name, email, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             password=password,
             avatar=avatar,
             user_role=UserRole.USER)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except:
        return False


# trong models
def add_receipt(cart):
    if cart:
        receipt = Receipt(customer_id=current_user.id)
        db.session.add(receipt)

        for p in list(cart.values()):
            detail = ReceiptDetail(receipt=receipt,
                                   product_id=int(p["id"]),
                                   quantity=p["quantity"],
                                   price=p["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False
