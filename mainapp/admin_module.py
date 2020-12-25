from mainapp import admin, db
from mainapp.models import Category, Book,  MyCategoryModelView,MyBookModelView, AboutUsView, LogoutView, MyAboutUsView, MyLogoutView
from flask_admin.contrib.sqla import ModelView

admin.add_view(MyCategoryModelView(Category, db.session))
admin.add_view(MyBookModelView(Book, db.session))
admin.add_view(MyAboutUsView(name="Thống kê"))
admin.add_view(MyLogoutView(name="Đăng xuất"))
