# from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from mainapp import db, admin
# from datetime import datetime
# from flask_login import UserMixin, logout_user, current_user
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import BaseView, expose
# from flask import redirect
#
#
# class Category(db.Model):
#     __tablename__ = 'category'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     books = relationship('Book', backref='category', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Book(db.Model):
#     __tablename__ = 'book'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     image = Column(String(255))
#     price = Column(Float, default=0)
#     description = Column(String(255))
#     active = Column(Boolean, default=True)
#     created_date = Column(Date, default=datetime.now())
#     category_id = Column(Integer, ForeignKey(Category.id))
#     receipt_details = relationship('ReceiptDetails', backref='book', lazy=True)
#
#
# class User(db.Model, UserMixin):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     avatar = Column(String(100))
#     active = Column(Boolean, default=True)
#     username = Column(String(100), nullable=False, unique=True)
#     password = Column(String(100), nullable=False)
#     receipts = relationship('Receipt', backref='user', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class CategoryModelView(ModelView):
#     can_export = True
#     form_columns = ('name', )
#
#
# class BookModelView(ModelView):
#     form_columns = ('name', 'image', 'price', 'active', 'created_date', 'category', )
#
#
# class AboutUsView(BaseView):
#     @expose("/")
#     def __index__(self):
#         return self.render("admin/about-us.html")
#
#
# class LogoutView(BaseView):
#     @expose('/')
#     def __index__(self):
#         logout_user()
#         return redirect('/admin')
#
#
# class Receipt(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(Date, default=datetime.today())
#     customer_id = Column(Integer, ForeignKey(User.id))
#     details = relationship('ReceiptDetails', backref='receipt', lazy=True)
#
#
# class ReceiptDetails(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id))
#     book_id = Column(Integer, ForeignKey(Book.id))
#     quantity = Column(Integer, default=0)
#     price = Column(Float, default=0)
#
#
# class MyCategoryModelView(CategoryModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# class MyBookModelView(BookModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# class MyAboutUsView(AboutUsView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# class MyLogoutView(LogoutView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# if __name__ == '__main__':
#     db.create_all()


from sqlalchemy import Column, Integer, Float, String, \
    Boolean, Enum, ForeignKey, Date, false
from flask import redirect
from sqlalchemy.orm import relationship
from mainapp import db
from flask_login import UserMixin, current_user, logout_user
from enum import Enum as UserEnum
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose


class SaleBase(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Category(SaleBase):
    __tablename__ = 'category'

    books = relationship('Book', backref='category', lazy=True)


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


class Book(SaleBase):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    image = Column(String(255))
    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    created_date = Column(Date, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id))
    receipt_details = relationship('ReceiptDetail', backref='book', lazy=True)


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(SaleBase, UserMixin):
    __tablename__ = 'user'

    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='customer', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(Date, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    details = relationship('ReceiptDetail',
                           backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)


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


class UserModelView(ModelView):
    form_columns = ('name', 'email', 'username', 'password', 'user_role', )


class ReceiptModelView(ModelView):
    can_create = False


class MyUserModelView(UserModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyReceiptModelView(ReceiptModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class Controller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def not_auth(self):
        return "your are not authorized the admin"


if __name__ == '__main__':
    db.create_all()