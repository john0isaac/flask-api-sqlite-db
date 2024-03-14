import logging
import os

from flask import Flask, abort, jsonify, request

from flaskapp.database.models import (
    Asset,
    Execution,
    TestCase,
    setup_db,
)

PAGINATION_PER_PAGE = 2


def paginate_results(flask_request, selection):
    page = flask_request.args.get("page", 1, type=int)
    start = (page - 1) * PAGINATION_PER_PAGE
    end = start + PAGINATION_PER_PAGE

    results = [result.format() for result in selection]
    paginated_results = results[start:end]

    return paginated_results


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # Load configuration for prod vs. dev
    is_prod_env = "RUNNING_IN_PRODUCTION" in os.environ
    if not is_prod_env:
        logging.info("Loading config.development.")
        app.config.from_object("flaskapp.config.development")
        setup_db(app)

        # db_drop_and_create_all(app)
    else:
        logging.info("Loading config.production.")
        app.config.from_object("flaskapp.config.production")
        setup_db(app)

        # db_drop_and_create_all(app)

    # ----------------------------------------------------------------------------#
    # Routes.
    # ----------------------------------------------------------------------------#

    @app.route("/")
    def index():
        return jsonify(
            {"success": True, "message": "Welcome to the test case management API"}
        )

    # ----------------------------------------------------------------------------#
    # Test cases.
    # ----------------------------------------------------------------------------#

    @app.route("/tests", methods=["GET"])
    def get_tests():
        selection = TestCase.query.order_by(TestCase.id).all()
        current_test_cases = paginate_results(request, selection)

        if len(current_test_cases) == 0:
            abort(404, "No data found in the database.")

        return jsonify(
            {
                "success": True,
                "test_cases": current_test_cases,
                "total_test_cases": len(TestCase.query.all()),
            }
        )

    @app.route("/tests", methods=["POST"])
    def create_test():
        body = request.get_json()
        if "name" not in body:
            abort(400, "The request body must contain 'name' field.")
        try:
            req_name = body.get("name")
            req_description = body.get("description", None)
            test_case = TestCase(name=req_name, description=req_description)
            test_case.insert()

            return jsonify(
                {
                    "success": True,
                    "test_case": test_case.format(),
                    "total_test_cases": len(TestCase.query.all()),
                }
            )
        except Exception as e:
            abort(422, str(e))

    @app.route("/tests/<int:test_case_id>", methods=["GET"])
    def get_test(test_case_id: int):
        test_case = TestCase.query.get(test_case_id)

        if not test_case:
            abort(404, "The requested test case was not found in the database.")

        return jsonify({"success": True, "test_case": test_case.format()})

    @app.route("/tests/<int:test_case_id>", methods=["PATCH"])
    def update_test(test_case_id: int):
        body = request.get_json()
        if "name" not in body:
            abort(400, "The request body must contain 'name' field.")

        test_case = TestCase.query.get(test_case_id)

        if not test_case:
            abort(404, "The requested test case was not found in the database.")

        try:
            req_name = body.get("name")
            req_description = body.get("description")
            test_case.name = req_name
            if req_description:
                test_case.description = req_description
            test_case.update()
            return jsonify(
                {
                    "success": True,
                    "test_case": test_case.format(),
                    "total_test_cases": len(TestCase.query.all()),
                }
            )
        except Exception as e:
            abort(422, str(e))

    @app.route("/tests/<int:test_case_id>", methods=["DELETE"])
    def delete_test(test_case_id: int):
        test_case = TestCase.query.get(test_case_id)

        if not test_case:
            abort(404, "The requested test case was not found in the database.")

        try:
            test_case.delete()
            if not TestCase.query.get(test_case_id):
                return jsonify(
                    {
                        "success": True,
                        "deleted_test_case_id": test_case_id,
                        "total_test_cases": len(TestCase.query.all()),
                    }
                )
        except Exception as e:
            abort(500, str(e))

    # ----------------------------------------------------------------------------#
    # Execution result.
    # ----------------------------------------------------------------------------#

    @app.route("/executions/<int:asset_id>", methods=["GET"])
    def get_executions(asset_id: int):
        asset = Asset.query.get(asset_id)
        if not asset:
            abort(404, "The requested asset was not found in the database.")

        executions = (
            Execution.query.filter(Execution.asset_id == asset_id)
            .join(Execution.test_case)
            .order_by(Execution.id)
            .all()
        )

        current_executions = []
        for execution in executions:
            current_executions.append(
                {
                    "id": execution.id,
                    "status": execution.status,
                    "details": execution.details,
                    "execution_date": execution.timestamp,
                    "test_case": {
                        "id": execution.test_case.id,
                        "name": execution.test_case.name,
                    },
                }
            )

        if len(executions) == 0:
            abort(404, "No data found in the database.")

        return jsonify(
            {
                "success": True,
                "executions": current_executions,
                "asset": asset.format(),
                "total_executions": len(executions),
            }
        )

    @app.route("/executions", methods=["POST"])
    def add_execution():
        body = request.get_json()
        if (
            "status" not in body
            or "details" not in body
            or "asset_id" not in body
            or "test_case_id" not in body
        ):
            abort(
                400,
                "The request body must contain 'status', 'details', 'asset_id', and 'test_case_id' fields.",
            )

        try:
            req_status = body.get("status")
            if req_status not in [True, False]:
                abort(400, "The status field must be a boolean.")
            req_asset_id = body.get("asset_id")
            req_test_case_id = body.get("test_case_id")

            asset = Asset.query.get(req_asset_id)
            if not asset:
                abort(404, "The asset was not found in the database.")

            test_case = TestCase.query.get(req_test_case_id)
            if not test_case:
                abort(404, "The test case was not found in the database.")

            req_details = body.get("details", "No details provided.")

            execution = Execution(
                asset_id=req_asset_id,
                test_case_id=req_test_case_id,
                status=req_status,
                details=req_details,
            )
            execution.insert()

            return jsonify(
                {
                    "success": True,
                    "execution": execution.format(),
                    "total_executions": len(Execution.query.all()),
                }
            )
        except Exception as e:
            abort(422, str(e))

    # ----------------------------------------------------------------------------#
    # Errors.
    # ----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False, "error": error.code, "message": error.description}
            ),
            error.code,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"success": False, "error": error.code, "message": error.description}
            ),
            error.code,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {"success": False, "error": error.code, "message": error.description}
            ),
            error.code,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": error.code, "message": error.description}
            ),
            error.code,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": error.code, "message": error.description}
            ),
            error.code,
        )

    return app
