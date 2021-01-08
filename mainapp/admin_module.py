from flask_login import current_user

from mainapp import admin, db, utils
# from mainapp.models import Category, Book, Receipt, \
#     ReceiptDetail, MyReceiptModelView, MyCategoryModelView,\
#     MyBookModelView, User, UserRole, MyUserModelView, UserModelView, \
#     LogoutView, MyAboutUsView, MyLogoutView
from mainapp.models import *

admin.add_view(MyCategoryModelView(Category, db.session))
admin.add_view(MyBookModelView(Book, db.session))
admin.add_view(MyAboutUsView(name="Thống kê"))
admin.add_view(MyUserModelView(User, db.session))
admin.add_view(MyReceiptModelView(Receipt, db.session))
admin.add_view(MyLogoutView(name="Đăng xuất"))
