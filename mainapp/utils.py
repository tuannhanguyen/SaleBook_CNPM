from mainapp.models import Book, Category


def read_book():
    return Book.query.all()


def cart_starts(cart):
    count, price = 0,0
    for p in cart.values():
        count = count + p["quantity"]
        price = price + p["price"] * p["quantity"]
    return count, price


