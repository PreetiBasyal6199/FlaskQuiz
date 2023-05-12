from app import app, db
from flask_restful import Api
from app.routes.quiz import CategoryResource, QuestionResource

api = Api(app)
if __name__ == '__main__':
    from app.routes.user import simple_page
    app.register_blueprint(simple_page)
    api.add_resource(CategoryResource, '/', '/category/', '/category/<category_id>/')
    api.add_resource(QuestionResource, '/', '/question/', '/question/<question_id>/')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
