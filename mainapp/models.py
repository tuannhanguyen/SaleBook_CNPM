from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mainapp import db, admin
from datetime import datetime
from flask_login import UserMixin, logout_user
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


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class CategoryModelView(ModelView):
    can_export = True
    form_columns = ('name', )


class AboutUsView(BaseView):
    @expose("/")
    def __index__(self):
        return self.render("admin/about-us.html")


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')


if __name__ == '__main__':
    db.create_all()
