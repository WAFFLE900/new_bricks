from flask import Flask, jsonify
from flask_cors import CORS

from flask_app import GlobalObjects

def create_app(test_mode=False):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {'origins': "*"}})

    if test_mode:
        # Testing mode
        app.config.from_pyfile()
    else:
        # DEV mode and PROD mode
        app.config.from_pyfile("config.py")

    # print(GlobalObjects)
    GlobalObjects.init_global_objects(app)
    print(GlobalObjects)

    from flask_app.api import (
        login,
        register,
        user_homepage,
        meeting_records
    )
    app.register_blueprint(login.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(user_homepage.bp)
    app.register_blueprint(meeting_records.bp)

    # Some testing APIs
    @app.route('/oauth_test', methods=['GET'])
    @GlobalObjects.flask_auth.login_required(optional=True)
    def index():
        '''The home page'''
        user = GlobalObjects.flask_auth.current_user()
        if user:
            return jsonify({"text":"歡迎使用Bricks專案管理實用工具",
                            "user":user.user_email})
        else:
            return jsonify({"text":"歡迎使用Bricks專案管理實用工具，請先登入"})

    # hello world route
    @app.route('/', methods=['GET'])
    def greetings():
        return ("Hello, world!")


    @app.route('/bricks', methods=['GET'])
    def bricks():
        return ("Bricks專案管理實用工具讚讚!")

    @app.route('/rollback', methods=['POST'])
    def rollback():
        try:
            response_object = {"status": "success"}
            GlobalObjects.db_session.rollback()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = str(e)
        return jsonify(response_object)

    return app



