# from app import ma
from marshmallow import Schema, fields, validates, ValidationError
from app.models import Category, Question, User
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


class UserCreateSchema(Schema):
    email = fields.String()
    password = fields.String()

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('User with this email already exists.')


class UserLoginSchema(Schema):
    email = fields.String()
    password = fields.String()

    @validates('email')
    def validate_email(self, email):
        if not User.query.filter_by(email=email).first():
            raise ValidationError('User with this email does not exists.')

    def validate(self, data):
        user = User.query.filter_by(email=data['email']).first()
        if not check_password_hash(user.password, data['password']):
            raise ValidationError({"password": ['Credentials does not match.']})
        return data


class CategorySchema(Schema):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at")


class CategoryUpdateSchema(Schema):
    class Meta:
        model = Category
        fields = ("name",)


class QuestionCreateSchema(Schema):
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


class QuestionListSchema(Schema):
    class Meta:
        model = Question
        fields = ("id", "question_text", "category_id", "answer", "score", "created_at")


class QuestionUpdateSchema(Schema):
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


class ResponseSchema(Schema):
    question_id = fields.Integer(required=True)
    answer = fields.String(required=True)

    @validates('question_id')
    def validate_question_id(self, value, **kwargs):
        category_id = request.view_args.get('category_id')
        category_obj = Category.query.get_or_404(category_id)
        question_obj: Question = Question.query.get_or_404(value)
        if question_obj not in category_obj.questions:
            raise ValidationError('Invalid question ID')


class QuizSchema(Schema):
    answers = fields.Nested(ResponseSchema, many=True)

    @validates('answers')
    def validate_answers(self, answers, **kwargs):
        category_id = request.view_args.get('category_id')
        category_obj = Category.query.get_or_404(category_id)
        # Get all the unique question IDs from the list of answers
        question_ids = set(answer['question_id'] for answer in answers)
        # Get all the question IDs for the quiz
        quiz_question_ids = set(question.id for question in category_obj.questions)
        # Check if the set of quiz question IDs is a subset of the set of answer question IDs
        if quiz_question_ids != question_ids:
            raise ValidationError('Quiz must include all questions.')
