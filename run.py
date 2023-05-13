from app import app, db
from flask_restful import Api
from app.routes.admin import CategoryResource, QuestionResource, CategoryRetrieveResource, QuestionDetailResource
from app.routes.play import CategoryListResource, QuestionListResource, PlayQuizAPI
api = Api(app)
if __name__ == '__main__':
    from app.routes.user import simple_page
    app.register_blueprint(simple_page)
    api.add_resource(CategoryResource, '/admin/category/', '/admin/category/', '/admin/category/<category_id>/')
    api.add_resource(CategoryRetrieveResource, '/admin/category-detail/<category_id>/')
    api.add_resource(QuestionResource, '/admin/question/', '/admin/question/', '/cms/question/<question_id>/')
    api.add_resource(QuestionDetailResource, '/admin/question-detail/<question_id>/')
    api.add_resource(QuestionListResource, '/question/<category_id>/')
    api.add_resource(CategoryListResource, '/category/')
    api.add_resource(PlayQuizAPI, '/play-quiz/<category_id>/')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
