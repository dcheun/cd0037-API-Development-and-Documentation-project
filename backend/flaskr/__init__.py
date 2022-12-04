import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(_request, selection):
    page = _request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    records = [rec.format() for rec in selection]
    current_records = records[start:end]

    return current_records


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        recs = Category.query.order_by(Category.id).all()
        data = [rec.format() for rec in recs]

        if len(data) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': data,
            'total_categories': len(data)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate(request, selection)

        if len(questions) == 0:
            abort(404)

        recs = Category.query.order_by(Category.id).all()
        categories = [rec.format() for rec in recs]

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_records = paginate(request, selection)

            return jsonify({
                'success': True,
                'deleted_id': question_id,
                'questions': current_records,
                'total_questions': len(selection)
            })
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        search = body.get('searchTerm')

        try:
            if search:
                matches = Question.query.filter(Question.question.ilike(f'%{search}%')).order_by(Question.id).all()
                current_records = paginate(request, matches)

                return jsonify({
                    'success': True,
                    'questions': current_records,
                    'total_questions': len(Question.query.all()),
                    'current_category': None
                })
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_records = paginate(request, selection)

                return jsonify({
                    'success': True,
                    'created_id': question.id,
                    'questions': current_records,
                    'total_questions': len(Question.query.all())
                })
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # @app.route('/questions/search', methods=['POST'])
    # def search_questions():
    #     body = request.get_json()
    #     search_term = body.get('searchTerm', '')
    #     matches = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
    #     current_records = paginate(request, matches)
    #
    #     return jsonify({
    #         'success': True,
    #         'questions': current_records,
    #         'total_questions': len(Question.query.all())
    #     })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
        current_records = paginate(request, selection)

        if len(current_records) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_records,
            'total_questions': len(Question.query.all()),
            'current_category': category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        body = request.get_json()
        previous_question_ids = body.get('previous_questions', [])
        print(f'previous_question_ids={previous_question_ids}')
        category_id = body.get('previous_category')

        recs = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous_question_ids)).all()
        print(f'recs={recs}')
        if not recs:
            question = None
        else:
            question = random.choice(recs).format()

        return jsonify({
            'success': True,
            'question': question,
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description or 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app
