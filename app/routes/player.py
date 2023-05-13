from app import db
from flask import request, jsonify
from app.models import Quiz, UserAnswer, Category, Question
from app.schema import CategorySchema, QuestionListSchema, QuizSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return CategorySchema(many=True).dump(categories)


class QuestionListResource(Resource):
    def get(self, category_id):
        category: Category = Category.query.get_or_404(category_id)
        return QuestionListSchema(many=True).dump(category.questions)


class PlayQuizAPI(Resource):
    @jwt_required()
    def post(self, category_id):
        quiz = Quiz(user_id=get_jwt_identity(), category_id=category_id, score=0)
        db.session.add(quiz)
        try:
            responses = QuizSchema().load(request.json)
            QuizSchema().validate(responses)
        except ValidationError as err:
            return err.messages, 400
        for response in responses['answers']:
            db.session.add(
                UserAnswer(quiz_id=quiz.id, question_id=response['question_id'], user_answer=response['answer']))
            question_obj: Question = Question.query.get(response['question_id'])
            if response['answer'].lower() == question_obj.answer.lower():
                quiz.score += question_obj.score
        db.session.commit()
        return {'score': quiz.score}
