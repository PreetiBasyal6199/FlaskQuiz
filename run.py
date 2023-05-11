from app import app, db

if __name__ == '__main__':
    from app.routes.user import simple_page
    app.register_blueprint(simple_page)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
