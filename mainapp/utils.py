from mainapp.models import Book, ReceiptDetails, Receipt
from mainapp import db
from flask_login import current_user


def read_book():
    return Book.query.all()


def cart_starts(cart):
    count, price = 0, 0
    if cart:
        for p in cart.values():
            count = count + p["quantity"]
            price = price + p["price"] * p["quantity"]
    return count, price


# trong models
def add_receipt(cart):
    # receipt = Receipt(customer_id=1)
    receipt = Receipt(customer_id=current_user.id)
    db.session.add(receipt)

    for p in list(cart.values()):
        detail = ReceiptDetails(quantity=p["quantity"],
                                price=p["price"],
                                book_id=p["id"],
                                receipt=receipt)
        db.session.add(detail)

    db.session.commit()



