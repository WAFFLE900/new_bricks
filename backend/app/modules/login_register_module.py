# app/modules/file_module.py
from flask import Blueprint
from . import *

#定義 登入註冊檔案的 Blueprint 名稱
login_register_module = Blueprint('login_register_module', __name__)

#hash password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

# auth = HTTPTokenAuth(scheme='Bearer')

# #verify token
# @auth.verify_token
# def verify_token(token):
#     conn = engine.connect()
#     print(jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256']))
#     try:
#         data = jwt.decode(token,
#                           current_app.config['SECRET_KEY'],
#                           algorithms=['HS256'])
#     except:
#         return False
    # return True

    # user=session.query(User).filter(User.user_email==data['user_email']).first()
    # if user is None:
    #     return False
    # return data['user_email']

# hello world route
@login_register_module.route('/', methods=['GET'])
def greetings():
    return ("Hello, world!")


@login_register_module.route('/bricks', methods=['GET'])
def bricks():
    return ("Bricks專案管理實用工具讚讚!")


@login_register_module.route('/login', methods=['GET', 'POST'])
def login():
    response_object = {'status': 'success'}
    response_object['message'] = "登入成功"
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "failure"
        response_object['message'] = "資料庫連線失敗"
        return jsonify(response_object)

    #取得檔案
    post_data = request.get_json()

    #對比信箱，如正確回傳 user_id
    try:
        user=session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        response_object['user_id'] = user.id
        user_password = user.user_password
        if user_password != post_data.get("user_password"):
            response_object['status'] = "failure"
            response_object['message'] = "您的密碼不正確，請再試一次"
            return jsonify(response_object)
    except IndexError:
        response_object['status'] = "failure"
        response_object['message'] = "您的帳號不正確，請再試一次"
        return jsonify(response_object)
    except:
        response_object['status'] = "failure"
        response_object['message'] = "SELECT user_id 失敗"
        return jsonify(response_object)

    token = jwt.encode(
        {
            'user_email': post_data.get("user_email"),
            'exp': int(time() + 60 * 60 * 24 * 30),
            'status': "success",
            'message': "登入成功"
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256')

    conn.close()
    return token


#註冊 --> 對比信箱及存入信箱、密碼及使用者名稱
@login_register_module.route('/register', methods=['POST'])
def register():
    response_object = {'status': 'success'}
    response_object['message'] = "信箱註冊成功"
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "failure"
        response_object['message'] = "資料庫連線失敗"
        return jsonify(response_object)
    post_data = request.get_json()
    if ((post_data.get("user_email") == None) |
        (post_data.get("user_password") == None) |
        (post_data.get("user_name") == None)):
        response_object['status'] = "failure"
        response_object['message'] = "有缺失信箱、密碼和使用者名稱回傳值"
        return jsonify(response_object)
    try:
        user=session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        if user is not None:
            response_object['status'] = "failure"
            response_object['message'] = "此信箱已被註冊過"
            return jsonify(response_object)

        new_user=User(user_email=post_data.get('user_email'),user_password=post_data.get('user_password'),
                      user_name=post_data.get('user_name'))
        session.add(new_user)
        response_object['user_id'] = new_user.id
    except:
        response_object['status'] = "failure"
        response_object['message'] = "註冊失敗，請稍後再試"
        return jsonify(response_object)

    token = jwt.encode(
        {
            'user_email': post_data.get("user_email"),
            'exp': int(time() + 60 * 60 * 24 * 30),
            'status': "success",
            'message': "登入成功"
        },
        app.config['SECRET_KEY'],
        algorithm='HS256')

    conn.close()
    return token


#加入使用者資訊 #取出資訊如果為list 要轉字串
@login_register_module.route('/register/survey', methods=['POST'])
def register_survey():
    response_object = {'status': 'success'}
    response_object['message'] = "使用者調查註冊成功"
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "failure"
        response_object['message'] = "資料庫連線失敗"
        return jsonify(response_object)
    post_data = request.get_json()
    try:
        user=session.query(User).filter(User.id==post_data.get('user_id')).first()
        if user is None:
            response_object['status']="failure"
            response_object['message']="找不到帳號"
            return jsonify(response_object)
        user.user_purpose=",".join(post_data.get("user_purpose"))
        user.user_identity=post_data.get("user_identity")
        user.user_otherTool=",".join(post_data.get("user_otherTool"))
        session.commit()

        response_object['user_email'] = user.user_email

    except Exception as e:
        response_object['status'] = "failure"
        response_object['message'] = "INSERT userInfo 失敗"
        logging.exception('Error at %s', 'division', exc_info=e)

    conn.close()
    return jsonify(response_object)