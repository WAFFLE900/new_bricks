from flask import Blueprint, request, jsonify, url_for, render_template_string

from flask_app import GlobalObjects
from flask_app.models import User
from flask_app.auth import make_JWT, hash_password

bp = Blueprint('login', __name__)

@bp.route('/frontend/google_login', methods=['GET'])
def google_login_entry():
    '''The function simulate the frontend URL which starts the Google OAuth2'''
    redirect_uri = url_for('login.google_callback', _external=True)
    # redirect_uri = redirect_uri.replace(":5000", ":8080")
    print(redirect_uri)
    return GlobalObjects.oauth.google.authorize_redirect(redirect_uri)


@bp.route('/frontend/google_callback', methods=['GET'])
def google_callback():
    '''
        The function simulates the frontend URL for the redirection of Google OAuth2.
        The response will make the browser put all the URL arguments from Google OAuth2
        into a form and request for the backend URL /backend/google_login to login.
    '''
    args_dict = request.args.to_dict()
    return render_template_string("""
        <html>
            <body onload="submitForm()">
                <form id="redirectForm" action="{{ url_for('login.google_login') }}" method="post">
                    {% for key, value in args_dict.items() %}
                        <input type="hidden" name="{{ key }}" value="{{ value }}">
                    {% endfor %}
                </form>
                <script>
                    function submitForm() {
                        document.getElementById('redirectForm').submit();
                    }
                </script>
            </body>
        </html>
    """, args_dict=args_dict)


@bp.route('/google_login', methods=['POST'])
def google_login():
    '''The backend URL for user to login with Google'''
    try:
        token = GlobalObjects.google_oauth.authorize_access_token()
    except:
        response_object = {
            'status':'failure',
            'message':"Google登入失敗"
        }
        return jsonify(response_object)

    # succeed to login with Google, then check the database for the login user
    user_info = token['userinfo']
    try:
        user =GlobalObjects.db_session.query(User).filter(User.user_email==user_info['email']).first()
        if user is None:
            # The user does NOT exist in the database, then register a new account
            user = User(user_email = user_info['email'],
                        user_name = user_info['name'])
            GlobalObjects.db_session.add(user)
            GlobalObjects.db_session.commit()
    except Exception as e:
        print(e)
        response_object = {
            'status':'failure',
            'message':str(e)
        }
        return jsonify(response_object)

    # email and password are verified
    response_object = {'status': "success",
                        'message': "登入成功"}
    response = jsonify(response_object)
    token = make_JWT(user.user_email) # issue a JWT token as authorization
    response.headers['Authorization'] = f"Bearer {token}"
    print(f"JWT : {response.headers['Authorization']}")
    return response


@bp.route('/bricks_login', methods=['POST'])
def bricks_login():
    post_data = request.get_json()
    try:
        user=GlobalObjects.db_session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        if user is None:
            response_object = {
                'status':'failure',
                'message':"您的帳號不正確"
            }
            return jsonify(response_object)
        elif user.user_password is None:
            response_object = {
                'status' : "failure",
                'message' : "請使用其他方式登入"
            }
            return jsonify(response_object)
        elif user.user_password != hash_password(post_data.get("user_password")):
            response_object = {
                'status' : "failure",
                'message' : "您的密碼不正確"
            }
            return jsonify(response_object)
    except Exception as e:
        print(e)
        response_object = {
            'status':'failure',
            'message':str(e)
        }
        return jsonify(response_object)

    # email and password are verified
    response_object = {'status': "success",
                        'message': "登入成功"}
    response = jsonify(response_object)
    token = make_JWT(post_data.get("user_email")) # issue a JWT token as authorization
    response.headers['Authorization'] = f"Bearer {token}"
    print(f"JWT : {response.headers['Authorization']}")
    return response
