# Quiz Application REST APIs
This is a Flask-based RESTful API that allows users to take quizzes and view their scores. The application allows an administrator to manage categories and questions.

## Functionality
### User actions:
- Get a list of categories.
- Get a list of questions for a specific category.
-Submit answers to a quiz and get a final score.

### Admin actions:
- Add, edit, and delete categories.
- Add, edit, and delete questions within each category.

## Security
The API endpoints are secured using JWT tokens for authentication and authorization. Users need to obtain a token by sending a valid email and password in a POST request to /login. The token needs to be included in the Authorization header of subsequent requests to access protected endpoints.

## API Endpoints
### The following API endpoints are available:

#### User endpoints:
- **GET /category/**: Get a list of all categories.
- **GET /question/<int:category_id>/** : Get a list of questions for a specific category.
- **POST /play-quiz/<int:category_id>/** : Start a new quiz for a specific category.
- **POST /signup/** : Create a new user
- **POST /login/** : Lets a user to login

#### Admin endpoints:
- **GET /admin/category/**: Get a list of all categories.
- **GET /admin/category-detail/<int:category_id>/** : Get details of a specific category.
- **POST /admin/category/**: Create a new category.
- **PATCH /admin/category/<int:category_id>/** : Update an existing category.
- **DELETE /admin/category/<int:category_id>/** : Delete a category.
- **GET /admin/question/** : Get a list of questions.
- **GET /question-detail/<int:question_id>/** : Get details of a specific question.
- **POST /admin/question/** : Create a new question.
- **PATCH /admin/question/<int:question_id>/**: Update an existing question.
- **DELETE /admin/question/<int:question_id>/**: Delete a question.

## Technologies Used
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- SQLAlchemy
- PostgreSQL

## Installation and Setup
1 Clone the repository.

```commandline
git clone https://github.com/PreetiBasyal6199/FlaskQuiz.git

git clone git@github.com:PreetiBasyal6199/FlaskQuiz.git
```


2 Create a virtual environment and activate it.
```commandline
virtualenv venv
source venv/bin/activate
```

3 Install the required packages.
```commandline
pip install -r requirements.txt
```

4. Create a PostgreSQL database and update the configuration file (config.py) with your database credentials.


Start the application.

```
python run.py
```
# Usage
1. Create an account by sending a POST request to /signup/ with a JSON payload containing your desired email and password.

```commandline
POST /signup/ HTTP/1.1
Content-Type: application/json

{
    "email": "jemail1@gmail.com",
    "password": "secret"
}
```
2. Authenticate by sending a POST request to /login/ with a JSON payload containing your email and password. You will receive a JWT token in response.

```commandline
POST /login/ HTTP/1.1
Content-Type: application/json

{
    "email": "jemail1@gmail.com",
    "password": "secret"
}
```
3. Get list of all categories
```commandline
GET /categories/ HTTP/1.1

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im9yYW5nZSIsImV4cCI6MTYyMzU5ODIwNywiaWF0IjoxNjIzNTkxNjA3fQ.HrEWGxRzT4We6ulIzoROZhbEKc1aHejU-yN2A6iSRVw
```
4. Create new category
```commandline
POST /admin/category/ HTTP/1.1

Content-Type: application/json

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

{
    "name": "News"
}
```

5. Update an existing category.
```commandline
PATCH /admin/category/1/ HTTP/1.1

Content-Type: application/json

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

{
    "name": "Sports (Updated)"
}

```
6. Delete a category
```commandline
DELETE /admin/category/1/ HTTP/1.1

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

```
7. Create new question for a specific category
```commandline
POST /admin/question/ HTTP/1.1

Content-Type: application/json

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

{
    "question_text": "Who won the last world cup?",
    "category_id": 1,
    "answer": "Australia"
    "score": 5
}

```

8. List all the question
```commandline
GET /admin/questions/ HTTP/1.1

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im9yYW5nZSIsImV4cCI6MTYyMzU5ODIwNywiaWF0IjoxNjIzNTkxNjA3fQ.HrEWGxRzT4We6ulIzoROZhbEKc1aHejU-yN2A6iSRVw
```

9. Update a question

```commandline
PATCH /admin/question/1/ HTTP/1.1

Content-Type: application/json

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

{
    "question_text": "Which is the highest Mountain?"
    "score": 10
}
```
10. Delete a question
```commandline
DELETE /admin/question/1/ HTTP/1.1

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

```

11. Get a list of all questions for a specific category.
```commandline
GET /questions/1/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

```

12. Play Quiz by choosing specific category
```commandline
POST /play-quiz/1/ HTTP/1.1

Content-Type: application/json

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjIzNTk4OTY4LCJpYXQiOjE2MjM1OTIzNjh9.RSBqKQkl6Y_T6_Nvo56kNWcK_xO7Hzoea-mGc26cB7c

{
  "answers": [
    {
      "question_id": 1,
      "answer": "Preeti"
    },
    {
      "question_id": 2,
      "answer": "Preeti"
    },
     {
      "question_id": 3,
      "answer": "Preeti"
    }
  ]
}
```
