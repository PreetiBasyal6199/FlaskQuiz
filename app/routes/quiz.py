from flask import jsonify, request, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from app import db
from app.models import Category, Question
from app.schema import CategorySchema, CategoryUpdateSchema, QuestionCreateSchema, QuestionListSchema, QuestionUpdateSchema
from marshmallow import ValidationError


class CategoryResource(Resource):

    # @jwt_required
    def get(self):
        cateogries = Category.query.all()
        categories_list = CategorySchema(many=True).dump(cateogries)
        return {"categories": categories_list}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        category = Category(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_dict())

    @jwt_required()
    def put(self, category_id):
        CategoryUpdateSchema().load(request.json)
        category = Category.query.get_or_404(category_id)
        category.name = request.json.get('name', category.name)
        db.session.commit()
        return CategorySchema().dump(category)

    @jwt_required()
    def delete(self, category_id):
        category_obj = Category.query.get_or_404(category_id)
        db.session.delete(category_obj)
        db.session.commit()
        return {'message': "Category Deleted Successfully"}, 204

    @jwt_required()
    def get(self, category_id):
        category_obj = Category.query.get_or_404(category_id)
        return CategorySchema().dump(category_obj)


class QuestionResource(Resource):
    def get(self):
        questions = Question.query.all()
        return QuestionListSchema(many=True).dump(questions)

    @jwt_required()
    def post(self):
        try:
            question_obj = QuestionCreateSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        ques = Question(**question_obj)
        db.session.add(ques)
        db.session.commit()

    @jwt_required()
    def patch(self, question_id):
        new_data = QuestionUpdateSchema().load(request.json, partial=True)
        question_obj = Question.query.get_or_404(question_id)
        for key, value in new_data.items():
            setattr(question_obj, key, value)
        db.session.commit()
        return QuestionListSchema().dump(question_obj)

    @jwt_required()
    def delete(self, question_id):
        question_obj = Question.query.get_or_404(question_id)
        db.session.delete(question_obj)
        db.session.commit()
        return{"message": "Question Deleted successfully."}, 204

    @jwt_required()
    def get(self, question_id):
        question_obj = Question.query.get_or_404(question_id)
        return QuestionListSchema().dump(question_obj)

