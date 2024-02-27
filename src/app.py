from flask import (
  Flask,
  request,
  abort,
  jsonify
)
import os
from src.database.models import (
    setup_db,
    db_drop_and_create_all,
    TestCase,
    Asset,
    Execution
)


app = Flask(__name__)

# Load configuration for prod vs. dev
is_prod_env = "RUNNING_IN_PRODUCTION" in os.environ
if not is_prod_env:
    print("Loading config.development.")
    app.config.from_object("src.config.development")
    setup_db(app)
    # db_drop_and_create_all(app)
else:
    print("Loading config.production.")
    app.config.from_object("src.config.production")
    setup_db(app)
    # db_drop_and_create_all(app)

PAGINATION_PER_PAGE = 10

def paginate_results(flask_request, selection):
    page = flask_request.args.get('page', 1, type=int)
    start =  (page - 1) * PAGINATION_PER_PAGE
    end = start + PAGINATION_PER_PAGE

    results = [result.format() for result in selection]
    paginated_results = results[start:end]

    return paginated_results

@app.route('/')
def index():
    return "Welcome to the Test Case Execution API"

@app.route('/tests')
def get_all_tests():
    selection = TestCase.query.order_by(TestCase.id).all()
    current_test_cases = paginate_results(request, selection)
    if len(current_test_cases) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'test_cases': current_test_cases,
        'total_test_cases': len(TestCase.query.all())
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

if __name__ == '__main__':
    app.run()
