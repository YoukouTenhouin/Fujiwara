from Fujiwara.handlers import Base
from Fujiwara.decorators import admin_requested

import tornado.web

class ListCategories(Base):
    def get(self):
        self.render('categories.html')

class AddCategory(Base):
    @admin_requested
    def post(self):
        name = self.get_argument('name')
        parent = self.get_argument('parent')
        self.mongo.categories.insert({'name':name,'parent':parent})
        self.redirect('/categories')
