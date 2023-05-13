from app import app, db
from flask_restful import Api
from app.routes.quiz import CategoryResource, QuestionResource, CategoryRetrieveResource, QuestionDetailResource
from app.routes.player import CategoryListResource, QuestionListResource, QuizResource, AnswerQuestionResource, PlayQuizAPI
api = Api(app)
if __name__ == '__main__':
    from app.routes.user import simple_page
    app.register_blueprint(simple_page)
    api.add_resource(CategoryResource, '/cms/category/', '/cms/category/', '/cms/category/<category_id>/')
    api.add_resource(CategoryRetrieveResource, '/cms/category-detail/<category_id>/')
    api.add_resource(QuestionResource, '/', '/cms/question/', '/cms/question/<question_id>/')
    api.add_resource(QuestionDetailResource, '/cms/question-detail/<question_id>/')
    api.add_resource(QuestionListResource, '/question/<category_id>/')
    api.add_resource(CategoryListResource, '/category/')
    api.add_resource(QuizResource, '/start-quiz/<category_id>/')
    api.add_resource(PlayQuizAPI, '/play/<quiz_id>/')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
