from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import User
from flask_app.auth import make_JWT, hash_password
import logging

bp = Blueprint('register', __name__)

#註冊 --> 對比信箱及存入信箱、密碼及使用者名稱
@bp.route('/register', methods=['POST'])
def bricks_register():
    response_object = {'status': 'success',
                       'message':'信箱註冊成功'}

    post_data = request.get_json()
    if ((post_data.get("user_email") == None) |
        (post_data.get("user_password") == None) |
        (post_data.get("user_name") == None)):
        response_object['status'] = "failure"
        response_object['message'] = "有缺失信箱、密碼和使用者名稱回傳值"
        return jsonify(response_object)
    try:
        user=GlobalObjects.db_session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        if user is not None:
            response_object['status'] = "failure"
            response_object['message'] = "此信箱已被註冊過"
            return jsonify(response_object)

        new_user=User(user_email = post_data.get('user_email'),
                      user_password = hash_password(post_data.get('user_password')),
                      user_name = post_data.get('user_name'))
        GlobalObjects.db_session.add(new_user)
        GlobalObjects.db_session.commit()
    except:
        response_object['status'] = "failure"
        response_object['message'] = "資料庫錯誤"
        return jsonify(response_object)

    # The registration succeeds
    response = jsonify(response_object)
    token = make_JWT(post_data.get("user_email")) # issue a JWT token as authorization
    response.headers['Authorization'] = f"Bearer {token}"
    return response


#加入使用者資訊 #取出資訊如果為list 要轉字串
@bp.route('/register/survey', methods=['POST'])
def register_survey():
    response_object = {'status': 'success'}
    response_object['message'] = "使用者調查註冊成功"

    # try:
    #     conn = engine.connect()
    # except:
    #     response_object['status'] = "failure"
    #     response_object['message'] = "資料庫連線失敗"
    #     return jsonify(response_object)
    
    post_data = request.get_json()
    try:
        user=GlobalObjects.db_session.query(User).filter(User.id==post_data.get('user_id')).first()
        if user is None:
            response_object['status']="failure"
            response_object['message']="找不到帳號"
            return jsonify(response_object)
        user.user_purpose=",".join(post_data.get("user_purpose"))
        user.user_identity=post_data.get("user_identity")
        user.user_otherTool=",".join(post_data.get("user_otherTool"))
        GlobalObjects.db_session.commit()

        response_object['user_email'] = user.user_email

    except Exception as e:
        response_object['status'] = "failure"
        response_object['message'] = "INSERT userInfo 失敗"
        logging.exception('Error at %s', 'division', exc_info=e)

    # conn.close()
    return jsonify(response_object)