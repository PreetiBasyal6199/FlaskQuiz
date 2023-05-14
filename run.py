from app import app, db
from flask_restful import Api
from app.routes.admin import CategoryResource, QuestionResource, CategoryRetrieveResource, QuestionDetailResource
from app.routes.play import QuestionListResource, PlayQuizAPI
api = Api(app)
if __name__ == '__main__':
    from app.routes.user import simple_page
    app.register_blueprint(simple_page)
    api.add_resource(CategoryResource, '/categories/', '/admin/category/', '/admin/category/<category_id>/')
    api.add_resource(CategoryRetrieveResource, '/admin/category-detail/<category_id>/')
    api.add_resource(QuestionResource, '/admin/questions/', '/admin/question/', '/admin/question/<question_id>/')
    api.add_resource(QuestionDetailResource, '/admin/question-detail/<question_id>/')
    api.add_resource(QuestionListResource, '/questions/<category_id>/')
    api.add_resource(PlayQuizAPI, '/play-quiz/<category_id>/')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
