# from app import db
from datetime import datetime
from app import db
from sqlalchemy import event


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return {self.email}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # questions = db.relationship('Question', backref='category_ref', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }


# @event.listens_for(Category, 'after_delete')
# def delete_questions_for_category(mapper, connection, target):
#     connection.execute(Question.__table__.delete().where(Question.category_id == target.id))
#     connection.execute(Quiz.__table__.delete().where(Quiz.category_id == target.id))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(164), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship("Category", backref=db.backref("questions", cascade="all,delete", lazy=True))
    answer = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'answer': self.answer,
            'category_id': self.category_id,
            'score': self.score,
            'created_at': self.created_at
        }


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship('Category', backref=db.backref('category', lazy=True, cascade="all,delete"))

    # questions = db.relationship('Question', secondary='quiz_questions')

    def get_questions(self):
        """
        Returns a list of all questions for the quiz.
        """
        questions = []
        for question in self.category.questions:
            questions.append(question)
        return questions


class UserAnswer(db.Model):
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    user_answer = db.Column(db.String(50))
    question = db.relationship('Question',
                               backref=db.backref('quiz_questions', lazy=True, cascade="all,delete"))
    quiz = db.relationship('Quiz',
                               backref=db.backref('user_answer', lazy=True, cascade="all,delete"))

    '''
        Adding Unique together between quiz_id and question_is as User can not answer the same question two times
        '''
    __table_args__ = (db.UniqueConstraint('quiz_id', 'question_id', name='uq_quiz_question'),)
