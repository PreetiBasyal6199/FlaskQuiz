from app import ma
from marshmallow import Schema, fields, validates, ValidationError
from app.models import Category, Question, Quiz, UserAnswer, User
from flask import request


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


class PlayQuizSchema(ma.Schema):
    quiz_id = fields.Integer(required=True)
    question_id = fields.Integer(required=True)
    answer = fields.String(required=True)

    @validates('quiz_id')
    def validate_quiz_id(self, value):
        current_user: User = self.context.get('current_user')
        quiz_obj: Quiz = Quiz.query.get_or_404(value)
        if quiz_obj.user_id != current_user:
            raise ValidationError('Invalid quiz ID')

    @validates('question_id')
    def validate_question_id(self, value):
        quiz_obj: Quiz = Quiz.query.get_or_404(self.context.get('quiz_id'))
        question_obj: Question = Question.query.get_or_404(self.context.get('question_id'))
        if question_obj not in quiz_obj.questions:
            raise ValidationError('Invalid question ID')


class ResponseSchema(Schema):
    question_id = fields.Integer(required=True)
    answer = fields.String(required=True)

    @validates('question_id')
    def validate_question_id(self, value, **kwargs):
        quiz_id = request.view_args.get('quiz_id')
        quiz_obj: Quiz = Quiz.query.get_or_404(quiz_id)
        question_obj: Question = Question.query.get_or_404(value)
        if question_obj not in quiz_obj.get_questions():
            raise ValidationError('Invalid question ID')


class QuizSchema(Schema):
    answers = fields.Nested(ResponseSchema, many=True)

    @validates('answers')
    def validate_answers(self, answers, **kwargs):
        quiz_id = request.view_args.get('quiz_id')
        # Get all the unique question IDs from the list of answers
        question_ids = set(answer['question_id'] for answer in answers)
        # Get all the question IDs for the quiz
        quiz_obj = Quiz.query.get_or_404(quiz_id)
        quiz_question_ids = set(question.id for question in quiz_obj.get_questions())
        # Check if the set of quiz question IDs is a subset of the set of answer question IDs
        if quiz_question_ids != question_ids:
            raise ValidationError('Quiz must include all questions.')
