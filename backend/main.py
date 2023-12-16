from dotenv import load_dotenv
from flask import Flask, current_app
from flask_cors import CORS
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz
import hashlib
import jwt
import logging
from flask import Flask, jsonify, request, current_app
from time import time
from sqlalchemy import create_engine, text
from models import *
from sqlalchemy.orm import *
from flask_httpauth import HTTPTokenAuth

load_dotenv()

# db_username = os.environ.get('DB_USERNAME')
# db_password = os.environ.get('DB_PASSWORD')
# db_host = os.environ.get('DB_HOST')
# db_port = os.environ.get('DB_PORT')
# db_name = os.environ.get('DB_NAME')

db_username = 'bricks'
db_password = 'NCCUgdsc1234!'
db_host = '35.194.196.179'
db_port = '3306'
db_name = 'bricksdata_test'


app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})
app.config['SECRET_KEY'] = 'secret'

#連線到伺服器上的 MySQL
db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url, echo=True)
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

auth = HTTPTokenAuth(scheme='Bearer')

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
    user=session.query(User).filter(User.user_email==data['user_email']).first()
    if user is None:
        return False
    return data['user_email']

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
    #取得檔案
    post_data = request.get_json()

    #對比信箱，如正確回傳 user_id
    try:
        user=session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        response_object['user_id'] = user.id
        user_password = user.user_password
        hash_user_password = hash_password(post_data.get('user_password'))
        print(user_password)
        if user_password != hash_user_password:
            response_object['status'] = "failure"
            response_object['message'] = "您的帳號密碼不正確，請再試一次"
            return jsonify(response_object)
    except IndexError:
        response_object['status'] = "failure"
        response_object['message'] = "您的帳號帳號不正確，請再試一次"
        return jsonify(response_object)
    except Exception as e:
        response_object['status'] = "failure"
        response_object['message'] = "SELECT user_id 失敗"
        print(str(e))
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

    return token


#註冊 --> 對比信箱及存入信箱、密碼及使用者名稱
@app.route('/register', methods=['POST'])
def register():
    response_object = {'status': 'success'}
    response_object['message'] = "信箱註冊成功"
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
        print(post_data.get('user_password'))
        hash_user_password = hash_password(post_data.get('user_password'))
        print(hash_user_password)
        new_user=User(user_email=post_data.get('user_email'),user_password=hash_user_password,
                      user_name=post_data.get('user_name'))
        session.add(new_user)
        session.commit()
        response_object['user_id'] = new_user.id
    except Exception as e:
        response_object['status'] = "failure"
        response_object['message'] = "註冊失敗，請稍後再試"
        print(str(e))
        return jsonify(response_object)

    # token = jwt.encode(
    #     {
    #         'user_email': post_data.get("user_email"),
    #         'exp': int(time() + 60 * 60 * 24 * 30),
    #         'status': "success",
    #         'message': "登入成功"
    #     },
    #     app.config['SECRET_KEY'],
    #     algorithm='HS256')

    return jsonify(response_object)


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


def row2dict(SQL_data):    
    data = []
    for row in SQL_data:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        data.append(d)
    return data

@app.route('/project_index', methods=['POST'])
def get_project():
    response_object = {"status": "success"}
    post_data = request.get_json()
    def get_data(sql):
        data = {}
        for project, project_sort in sql:
            d = {}
            for column in project.__table__.columns:
                d[column.name] = str(getattr(project, column.name))
            del d['project_type']
            d['type_id'] = project_sort.type_id
            if project.project_type not in data.keys():
                data[project.project_type] = []
            data[project.project_type].append(d)
        return data
    if post_data.get("project_status") == "normal":
        try:
            SQL_q = session.query(Project, ProjectSort).join(ProjectSort, Project.project_type==ProjectSort.project_type).filter(
                Project.user_id==post_data.get("user_id"),
                Project.project_trashcan==0,
                Project.project_ended==0,
                ProjectSort.user_id==post_data.get("user_id")
            ).order_by(
                ProjectSort.project_type_sort.asc(),
                Project.project_edit_date.desc()
            ).all()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            return jsonify(response_object), 404 
        data = get_data(SQL_q) 
        response_object["items"] = data
        response_object["message"] = "正在進行專案"

    elif post_data.get("project_status") == "ended":
        try:
            SQL_q=session.query(Project, ProjectSort).join(ProjectSort,Project.project_type==ProjectSort.project_type).filter(
                Project.user_id==post_data.get("user_id"),
                Project.project_trashcan==0,
                Project.project_ended==1,
                ProjectSort.user_id==post_data.get("user_id")
            ).order_by(
                ProjectSort.project_type_sort.asc(),
                Project.project_edit_date.desc()
            ).all()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            return jsonify(response_object), 404
        data = get_data(SQL_q)    
        response_object["items"] = data
        response_object["message"] = "已結束專案"

    elif post_data.get("project_status") == "trashcan":
        try:
            time_delta = datetime.now() - relativedelta(months=1)
            in_month_SQL_data = session.query(Project).filter(
                Project.user_id == post_data.get("user_id"),
                Project.project_trashcan == 1,
                Project.project_edit_date>=time_delta
            ).order_by(
                Project.project_edit_date.desc()
            ).all()

            not_in_month_SQL_data = session.query(Project).filter(
                Project.user_id == post_data.get("user_id"),
                Project.project_trashcan == 1,
                Project.project_edit_date<time_delta
            ).order_by(
                Project.project_edit_date.desc()
            ).all()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            return jsonify(response_object), 404
        print(in_month_SQL_data)
        in_month_data = row2dict(in_month_SQL_data)
        not_in_month_data = row2dict(not_in_month_SQL_data)
        response_object["item"] = {
            "in_month":in_month_data,
            "not_int_month":not_in_month_data
        }
        response_object["message"] = "垃圾桶"

    return jsonify(response_object)


@app.route("/set_project_end", methods=["POST"])
def set_end():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        session.query(Project).filter(Project.id==post_data.get("project_id")).update({"project_ended":True})
        session.commit()
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "SQL 搜尋失敗，找不到專案"
        print(str(e))
        return jsonify(response_object), 404
    response_object["message"] = "修改成功"
    return jsonify(response_object)

@app.route('/add_project', methods=['POST'])
def add_project():
    response_object = {"status": "success"}
    post_data = request.get_json()
    try:
        print(session.query(User).all())
        new_project = Project(project_type=post_data.get("project_type"), project_image=post_data.get("project_image"),
                            project_name=post_data.get("project_name"), project_trashcan=post_data.get("project_trashcan"),
                            project_ended=post_data.get("project_ended"), project_edit=post_data.get("project_isEdit"),
                            project_visible=post_data.get("project_isVisible"), project_comment=post_data.get("project_isComment"),
                            user_id=post_data.get("user_id"))
        session.add(new_project)
        session.flush()
        session.commit()
        print(new_project.id)
        
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        return jsonify(response_object), 404
    response_object["message"] = "新增{}成功".format(post_data.get("project_name"))
    return jsonify(response_object)


@app.route("/add_type", methods=["POST"])
def add_type():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        session.query(Project).filter(Project.id==post_data.get("project_id")).update({"project_type":post_data.get("project_type")})
        session.commit()

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        return jsonify(response_object), 404
    response_object["message"] = "新增{}成功".format(post_data.get("project_type"))
    return jsonify(response_object)

@app.route("/edit_type", methods=["POST"])
def set_type():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        project_count = session.query(Project).filter(Project.project_type == post_data.get("old_project_type")).count()
        if project_count == 0:
            response_object["status"] = "failed"
            response_object["message"] = "輸入類別名稱錯誤"
            return jsonify(response_object)
        session.query(Project).filter(Project.project_type == post_data.get("old_project_type")).update({"project_type": post_data.get("project_type")})

        session.commit()
        response_object["message"] = f"{post_data.get('old_project_type')}成功修改成{post_data.get('project_type')}"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)


@app.route("/trashcan_recover", methods=["POST"])
def recover():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=0
        session.commit()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)

@app.route("/to_trashcan", methods=["POST"])
def trashcan():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        project=session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=1
        session.commit()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)

    return jsonify(response_object)

@app.route('/search', methods=['POST'])
def search():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    
    try:
        rank_score = []
        status = post_data.get("search_status")
        if status == "normal":
            project_list = session.query(Project).filter(Project.user_id == post_data.get("user_id"), Project.project_ended == False, Project.project_trashcan == False).all()
        elif status == "ended":
            project_list = session.query(Project).filter(Project.user_id == post_data.get("user_id"), Project.project_ended == True, Project.project_trashcan == False).all()
        elif status == "trashcan":
            project_list = session.query(Project).filter(Project.user_id == post_data.get("user_id"), Project.project_trashcan == True).all()
        elif status == "":
            project_list = session.query(Project).filter(Project.user_id == post_data.get("user_id")).all()
        
        for project in project_list:
            d = {}
            for column in project.__table__.columns:
                d[column.name] = str(getattr(project, column.name))
            

            # 計算相似度（使用 fuzz.ratio 或 fuzz.token_sort_ratio）
            score = fuzz.ratio(project.project_name, post_data.get("search_content"))
            d['score'] = score
            rank_score.append(d)
            print(project.id, post_data.get("search_content"), project.project_name, fuzz.ratio(project.project_name, post_data.get("search_content")))
        
        sorted_rank = sorted(rank_score, key = lambda x:x.get('score'), reverse=True)
        for i in sorted_rank:
            print(i["project_name"])
        

    except Exception as e:
        response_object['status'] = "failure"
        print(str(e))
    
    response_object['items'] = sorted_rank
    return jsonify(response_object) 




if __name__ == "__main__":
    app.run(debug=True)
