import json
import pymysql
from turtle import pos
from models import *
from dotenv import load_dotenv
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
import hashlib
import jwt
import logging
import os
from sqlalchemy import create_engine, text
from time import time
from sqlalchemy.orm import sessionmaker

load_dotenv()

'''
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
'''

db_username = 'root'
db_password = '123'
db_host = '127.0.0.1'
db_port = '3306'
db_name = 'bricks_test'


app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})
app.config['SECRET_KEY'] = 'secret'

#連線到伺服器上的 MySQL
# {db_password}
db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
# db_url = f"mysql+pymysql://{db_username}:@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

Session=sessionmaker(bind=engine)
session=Session()

app.config.from_object(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

#hash password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

#verify token
@auth.verify_token
def verify_token(token):
    conn = engine.connect()
    print(jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']))
    try:
        data = jwt.decode(token,
                          app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except:
        return False
    # return True

    user=session.query(User).filter(User.user_email==data['user_email']).first()
    if user is None:
        return False
    return data['user_email']

DATA = [
    {
    'account':'RuCiCa',
    'password': 'RuCiCa0307'
    }
]

DATA = [
    {
    'account':'RuCiCa',
    'password': 'RuCiCa0307'
    }
]


# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return ("Hello, world!")


@app.route('/bricks', methods=['GET'])
def bricks():
    return ("Bricks專案管理實用工具讚讚!")


@app.route('/login', methods=['GET', 'POST'])
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
        app.config['SECRET_KEY'],
        algorithm='HS256')
    
    conn.close()
    return token


#註冊 --> 對比信箱及存入信箱、密碼及使用者名稱
@app.route('/register', methods=['POST'])
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
@app.route('/register/survey', methods=['POST'])
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


@app.route('/project_index', methods=['POST'])
def get_project():
    conn = engine.connect()
    response_object = {"status": "success"}
    post_data = request.get_json()
    found = False
    
    if post_data.get("project_status") == "normal":
        data=Project.query.join(ProjectSort,Project.project_type==ProjectSort.project_type).filter(
            Project.user_id==post_data.get("user_id"),
            Project.project_trashcan==0,
            Project.project_ended==0,
            ProjectSort.user_id==post_data.get("user_id")
        ).order_by(
            ProjectSort.project_type_sort.asc(),
            Project.project_edit_date.desc()
        ).all()
        conn.close()
        found = True
        response_object["items"] = data

    if post_data.get("project_status") == "ended":
        data=Project.query.join(ProjectSort,Project.project_type==ProjectSort.project_type).filter(
            Project.user_id==post_data.get("user_id"),
            Project.project_trashcan==0,
            Project.project_ended==1,
            ProjectSort.user_id==post_data.get("user_id")
        ).order_by(
            ProjectSort.project_type_sort.asc(),
            Project.project_edit_date.desc()
        ).all()
        conn.close()
        found = True
        response_object["items"] = data


    if post_data.get("project_status") == "trashcan":
        month_data=Project.query.filter(
            Project.user_id==post_data.get("user_id"),
            Project.project_trashcan==1,
            Project.project_edit_date>=func.date_sub(func.now(),interval=1,unit='month')
        ).order_by(
            Project.project_edit_date.desc()
        ).all()

        not_month_data=Project.query.filter(
            Project.user_id==post_data.get("user_id"),
            Project.project_trashcan==1,
            Project.project_edit_date<func.date_sub(func.now(),interval=1,unit='month')
        ).order_by(
            Project.project_edit_date.desc()
        ).all()

        found = True
        response_object["in_month"] = month_data
        response_object["not_in_month"] = not_month_data
        response_object["message"] = "垃圾桶"
        conn.close()
    
    if found == False:
        response_object["status"] = "failed"
        response_object["message"] = "沒找到"

    return jsonify(response_object)


@app.route("/set_project_end", methods=["POST"])
def set_end():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object['status']="failed"
            response_object["message"]="找不到專案"
        project.project_ended=1
        session.commit()
        conn.close()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route('/add_project', methods=['POST'])
def add_project():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()

        new_project=Project(project_type=post_data.get("project_type"), project_image=post_data.get("project_image"),
                            project_name=post_data.get("project_name"), project_trashcan=post_data.get("project_trashcan"),
                            project_ended=post_data.get("project_ended"), project_isEdit=post_data.get("project_isEdit"),
                            project_isVisible=post_data.get("project_isVisible"), project_isCommit=post_data.get("project_isComment"),
                            user_id=post_data.get("user_id"))
        session.add(new_project)
        session.commit()
        conn.close()
        response_object["message"] = "新增{}成功".format(post_data.get("project_name"))

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/add_type", methods=["POST"])
def add_type():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()

        last=ProjectSort.query.with_entities(func.max(ProjectSort.project_type_sort)).filter(
            ProjectSort.user_id==post_data.get("user_id"),
            ProjectSort.project_ended==post_data.get("project_ended")
        ).scalar()

        last_id=ProjectSort.query.with_entities(func.max(ProjectSort.type_id)).filter(
            ProjectSort.user_id==post_data.get("user_id"),
            ProjectSort.project_ended==post_data.get("project_ended")
        ).scalar()

        sort = last + 1
        id = last_id + 1

        new_project_sort=ProjectSort(type_id=id,project_type=post_data.get("project_type"),project_type_sort=sort,
                                     user_id=post_data.get("user_id"),project_ended=post_data.get("project_ended"))
        db.session.add(new_project_sort)
        db.session.commit()
        conn.close()
        response_object["message"] = "新增成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/edit_type", methods=["POST"])
def set_type():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_type=post_data.get("project_type")
        session.commit()
        conn.close()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/trashcan_recover", methods=["POST"])
def recover():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=0
        session.commit()
        conn.close()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/type_reindex", methods=["POST"])
def type_reindex():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()
        
        for item in post_data.get("type_sort"):
            id = item["id"]
            project_type_sort = item["project_type_sort"]
            project_sort=session.query(ProjectSort).filter( ProjectSort.type_id==post_data.get("user_id"),
                                                           ProjectSort.user_id==post_data.get("project_ended"),
                                                           ProjectSort.project_ended==post_data.get("project_ended")).first()
            if project_sort is None:
                response_object["status"]="failed"
                response_object["message"]="找不到專案類型"
                return jsonify(response_object)
            project_sort.project_type_sort=project_type_sort
            print("sort:{}, type_id:{}, user_id:{}".format(project_type_sort, id, post_data.get("user_id")))
        session.commit()
        conn.close()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/to_trashcan", methods=["POST"])
def trashcan():
    response_object = {"status": "success"}
    try:
        conn = engine.connect()
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=1
        session.commit()
        conn.close()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/personal_setting", methods=["POST"])
def personal_setting():
    try:
        conn = engine.connect()
        response_object = {"status": "success"}
        post_data = request.get_json()
        
        user=session.query(User).filter_by(id=post_data.get("user_id")).first()
        if user is None:
            response_object["status"]="failed"
            response_object["message"]="找不到用戶"
            return jsonify(response_object)
        data=user.to_dict()
        conn.close()
        response_object["items"] = data
    
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route('/notification', methods=['POST'])
def notification():
    response_object = {'status': 'success'}
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "connect failure"
    user_id = request.get_json().get("user_id")
    try:
        data=Notification.query.join(Mention,Notification.id==Mention.notification_id).filter(
            Mention.notification_recipient_id==user_id).all()
        response_object['items'] = data
    except:
        response_object['status'] = "algorithm failure"
    conn.close()
    return jsonify(response_object)


@app.route('/search', methods=['POST'])
def search():

    response_object = {'status': 'success'}
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "connect failure"

    global search_content
    search_content = request.get_json().get("search_content")
    S_DATA = []

    try:
        data=Project.query.all()
        for project_info in data:
            if lcs(project_info) > 0:
                S_DATA.append(project_info)
        S_DATA.sort(key=lcs, reverse=True)
        response_object['items'] = S_DATA
    except:
        response_object['status'] = "algorithm failure"

    conn.close()
    return jsonify(response_object)


def lcs(data):
    str1 = search_content
    str2 = data['project_name']
    str1_len = len(str1)
    str2_len = len(str2)

    dp = [[0 for x in range(str1_len + 1)] for y in range(str2_len + 1)]

    for i in range(1, str2_len + 1):
        for j in range(1, str1_len + 1):
            if (str1[j - 1] == str2[i - 1]):
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[str2_len][str1_len]




if __name__ == "__main__":
    app.run(debug=True)
