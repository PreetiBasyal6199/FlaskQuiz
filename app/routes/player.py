from app import db, ma
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
from app.models import Quiz, UserAnswer, Category, Question
from app.schema import CategorySchema, QuestionListSchema, PlayQuizSchema, ResponseSchema, QuizSchema
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


class QuizResource(Resource):
    @jwt_required()
    def post(self, category_id):
        quiz = Quiz(user_id= get_jwt_identity(), category_id=category_id, score=0)
        db.session.add(quiz)
        db.session.commit()
        return {"quiz": quiz.id}


class AnswerQuestionResource(Resource):
    def post(self, quiz_id):
        try:
            ans = PlayQuizSchema().load(request.json)
            quiz_obj: Quiz = Quiz.query.get(quiz_id)
            question_obj: Question = Question.query.get(request.json['question_id'])
            answer = request.json['answer']
            UserAnswer(**ans)
            if answer != question_obj.answer:
                return {"message": "Opps You have answered incorrectly."}
            quiz_obj.score = question_obj.score
            return {"message": "Congrats You have answered correctly."}

        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'You have already answered this question'}), 400



class PlayQuizAPI(Resource):
    def post(self, quiz_id):
        quiz_obj = Quiz.query.get_or_404(quiz_id)
        # if
        try:
            responses = QuizSchema().load(request.json)
        except ValidationError as err:
            return {'message': err.messages}, 400
        score = 0
        for response in responses['answers']:
            db.session.add(
                UserAnswer(quiz_id=quiz_id, question_id=response['question_id'], user_answer=response['answer']))
            db.session.commit()
            question_obj: Question = Question.query.get(response['question_id'])
            if response['answer'].lower() == question_obj.answer.lower():
                score += 1
        return {'score': score}














