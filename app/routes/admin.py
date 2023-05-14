from flask import jsonify, request, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from app import db
from app.models import Category, Question
from app.schema import CategoryListSchema, CategoryCreateUpdateSchema, QuestionCreateSchema, QuestionListSchema, \
    QuestionUpdateSchema
from marshmallow import ValidationError
from app.decorator import is_admin


class CategoryResource(Resource):

    @jwt_required()
    def get(self):
        """
        Get list of all categories
        """
        cateogries = Category.query.all()
        categories_list = CategoryListSchema(many=True).dump(cateogries)
        return {"categories": categories_list}

    @is_admin
    @jwt_required()
    def post(self):
        """
        Create a new category.
        ---
        parameters:
          - name: name
            in: request data
            required: true
            type: string
        """
        try:
            category_schema = CategoryCreateUpdateSchema().load(request.json)
            category_obj = Category(**category_schema)
            db.session.add(category_obj)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return CategoryListSchema().dump(category_obj)

    @is_admin
    @jwt_required()
    def patch(self, category_id):
        """
       Updates a new category.
       ---
       parameters:
         - name: category_id
           in: path
           required: true
           type: int
         - name: name
           in: request data
           required: true
           type: string
        """
        try:
            CategoryCreateUpdateSchema().load(request.json)
            category = Category.query.get(category_id)
            if not category:
                abort(404, "Invalid Category ID.")
            category.name = request.json.get('name', category.name)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return CategoryListSchema().dump(category)

    @is_admin
    @jwt_required()
    def delete(self, category_id):
        """
        Delete a category by ID.
        ---
        parameters:
          - name: category_id
            in: path
            description: ID of the category to delete
            required: true
            type: integer
        responses:
          204:
            description: No Content.
          404:
            description: Invalid category ID.
        """
        category_obj = Category.query.get(category_id)
        if not category_obj:
            abort(404, "Invalid category ID.")
        db.session.delete(category_obj)
        db.session.commit()
        return {'message': "Category Deleted Successfully"}, 204


class CategoryRetrieveResource(Resource):
    @is_admin
    @jwt_required()
    def get(self, category_id):
        category_obj = Category.query.get(category_id)
        if not category_obj:
            abort(404, "Invalid Category ID")
        return CategoryListSchema().dump(category_obj)


class QuestionResource(Resource):
    @is_admin
    def get(self):
        """
        Get list of all questions
        """
        questions = Question.query.all()
        return QuestionListSchema(many=True).dump(questions)

    @is_admin
    @jwt_required()
    def post(self):
        """
        Create new question to a category
        :parameter
            - name: category_id
              in: request data
              type: int
              required: True
            - name: question_text
              in: request data
              type: String
              required: True
            - name: answer
              in: request data
              type: String
              required: True
            - name: score
              in: request data
              type: Int
              required: True


        :responses
          200:
            description: Returns the Question that is created
          404:
            description: Invalid Question ID
        """
        try:
            question_obj = QuestionCreateSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        ques = Question(**question_obj)
        db.session.add(ques)
        db.session.commit()
        return QuestionListSchema().dump(ques)

    @is_admin
    @jwt_required()
    def patch(self, question_id):
        """

        :param question_id:
        :return: Updated question object detail
        """
        new_data = QuestionUpdateSchema().load(request.json, partial=True)
        question_obj = Question.query.get(question_id)
        if not question_obj:
            abort(404, "Invalid question ID")
        for key, value in new_data.items():
            setattr(question_obj, key, value)
        db.session.commit()
        return QuestionListSchema().dump(question_obj)

    @is_admin
    @jwt_required()
    def delete(self, question_id):
        """

        :param question_id:
        """
        question_obj = Question.query.get_or_404(question_id)
        db.session.delete(question_obj)
        db.session.commit()
        return {"message": "Question Deleted successfully."}, 204


class QuestionDetailResource(Resource):
    @is_admin
    @jwt_required()
    def get(self, question_id):
        """
        Gets a detail of specific Question
        :param question_id:
        :return
            204:
                description: No Content
            404:
                description: Invalid question ID

        """
        question_obj = Question.query.get(question_id)
        if not question_obj:
            abort(404, "Invalid question ID")
        return QuestionListSchema().dump(question_obj)
