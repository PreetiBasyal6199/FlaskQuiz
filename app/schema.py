from app import ma
from marshmallow import Schema, fields, validates, ValidationError
from app.models import Category, Question


class CategorySchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at")


class CategoryUpdateSchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("name",)


class QuestionCreateSchema(ma.Schema):
    question_text = fields.String(required=True)
    category_id = fields.Integer(required=True)
    answer = fields.String(required=True)
    score = fields.Integer(required=True)

    class Meta:
        model = Question
        fields = ("question_text", "category_id", "answer", "score")

    @validates('category_id')
    def validate_category_id(self, value):
        if not Category.query.get(value):
            raise ValidationError('Invalid category ID')


class QuestionListSchema(ma.Schema):
    class Meta:
        model = Question
        fields = ("id", "question_text", "category_id", "answer", "score", "created_at")


class QuestionUpdateSchema(ma.Schema):
    question_text = fields.String()
    category_id = fields.Integer()
    answer = fields.String()
    score = fields.Integer()

    # class Meta:
    #     model = Question
    #     fields = ("question_text", "category_id", "answer", "score")

    @validates('category_id')
    def validate_category_id(self, value):
        if not Category.query.get(value):
            raise ValidationError('Invalid category ID')
