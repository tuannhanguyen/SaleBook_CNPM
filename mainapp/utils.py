from mainapp.models import Book, Category


def read_book():
    return Book.query.all()


def read_cate():
    return Category.query.all()