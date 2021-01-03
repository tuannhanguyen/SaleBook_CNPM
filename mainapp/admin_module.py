from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

from flask_admin.menu import MenuLink

from mainapp import admin, db
from mainapp.models import Category, Book, Controller, Receipt, ReceiptDetail, MyReceiptModelView, MyCategoryModelView, MyBookModelView, User, MyUserModelView, UserModelView, LogoutView, MyAboutUsView, MyLogoutView
from flask_admin.contrib.sqla import ModelView

path = op.join(op.dirname(__file__), 'static')
admin.add_view(MyCategoryModelView(Category, db.session))
admin.add_view(MyBookModelView(Book, db.session))
admin.add_view(MyAboutUsView(name="Thống kê"))
admin.add_view(MyUserModelView(User, db.session))
admin.add_view(MyReceiptModelView(Receipt, db.session))
admin.add_view(MyLogoutView(name="Đăng xuất"))
