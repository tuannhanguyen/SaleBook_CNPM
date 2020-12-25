from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mainapp import db, admin
from datetime import datetime
from flask_login import UserMixin, logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    image = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    created_date = Column(Date, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id))
    receipt_details = relationship('ReceiptDetails', backref='book', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class CategoryModelView(ModelView):
    can_export = True
    form_columns = ('name', )


class BookModelView(ModelView):
    form_columns = ('name', 'image', 'price', 'active', 'created_date', 'category', )


class AboutUsView(BaseView):
    @expose("/")
    def __index__(self):
        return self.render("admin/about-us.html")


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    book_id = Column(Integer, ForeignKey(Book.id))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


class MyCategoryModelView(CategoryModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyBookModelView(BookModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAboutUsView(AboutUsView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyLogoutView(LogoutView):
    def is_accessible(self):
        return current_user.is_authenticated


if __name__ == '__main__':
    db.create_all()
