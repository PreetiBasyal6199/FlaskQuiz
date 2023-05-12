from app import ma
from app.models import Category


class CategorySchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at")

class CategoryUpdateSchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("name", )
