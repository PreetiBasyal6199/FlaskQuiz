from flask import jsonify, request, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from app import db
from app.models import Category
from app.schema import CategorySchema, CategoryUpdateSchema


class CategoryResource(Resource):

    # @jwt_required
    def get(self):
        cateogries = Category.query.all()
        category_schema = CategorySchema(many=True)
        categories_list = category_schema.dump(cateogries)
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
