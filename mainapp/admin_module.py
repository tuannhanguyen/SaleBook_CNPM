from mainapp import admin, db
from mainapp.models import Category, Book,  CategoryModelView, AboutUsView, LogoutView
from flask_admin.contrib.sqla import ModelView

admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(AboutUsView(name="gioi thieu"))
admin.add_view(LogoutView(name="Dang xuat"))
