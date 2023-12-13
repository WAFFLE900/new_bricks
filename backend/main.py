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
from authlib.integrations.flask_client import OAuth

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

# Google OAuth configs
oauth = OAuth(app)
oauth.init_app(app)
google_oauth = oauth.register(
    name='google', # name of this method
    client_id='638644428386-al4ccfos6s82t0arpr82p5gan6rcfa6d.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://www.googleapis.com/oauth2/v4/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://accounts.googleapis.com/oauth2/v3',
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
    jwk_uri='https://www.googleapis.com/oauth2/v3/certs'
)


# Flask authentication configs
app.config.from_object(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    '''decode the JWT and verify the user identity'''
    try:
        data = jwt.decode(token,
                          app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except:
        return False

    if time() > data['exp']:
        # the JWT is expired
        return False
    
    user = session.query(User).filter(User.user_email==data['user_email']).first()
    if user is None:
        return False
    return user

@auth.error_handler
def auth_error(status):
    response_object = {
        "message":"Access Denied",
        "status":"failure"
    }
    if status == 403:
        response_object['message'] = "Permission Denied"
    return jsonify(response_object), status



# Utility functions
def hash_password(password):
    '''The function hashes the input password'''
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

def make_JWT(user_email):
    '''The function create the JWT for a login user'''
    token = jwt.encode(
        {
            'user_email': user_email,
            'exp': int(time() + 60 * 60 * 24 * 30)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256')
    return token



# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return ("Hello, world!")


@app.route('/bricks', methods=['GET'])
def bricks():
    return ("Bricks專案管理實用工具讚讚!")


@app.route('/google_login', methods=['POST'])
def google_login():
    '''The backend URL for user to login with Google'''
    try:
        token = google_oauth.authorize_access_token()
    except:
        response_object = {
            'status':'failure',
            'message':"Google登入失敗"
        }
        return jsonify(response_object)
    
    # succeed to login with Google, then check the database for the login user
    user_info = token['userinfo']
    try:
        user = session.query(User).filter(User.user_email==user_info['email']).first()
        if user is None:
            # The user does NOT exist in the database, then register a new account
            user = User(user_email = user_info['email'],
                        user_name = user_info['name'])
            session.add(user)
            session.commit()
    except:
        response_object = {
            'status':'failure',
            'message':"資料庫錯誤"
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


@app.route('/bricks_login', methods=['POST'])
def bricks_login():
    post_data = request.get_json()
    try:
        user=session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        if user.user_password is None:
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
    except exc.NoResultFound:
        response_object = {
            'status':'failure',
            'message':"您的帳號不正確"
        }
        return jsonify(response_object)
    except:
        response_object = {
            'status':'failure',
            'message':"資料庫錯誤"
        }
        return jsonify(response_object)

    # email and password are verified
    response_object = {'status': "success",
                        'message': "登入成功"}
    response = jsonify(response_object)
    token = make_JWT(post_data.get("user_email")) # issue a JWT token as authorization
    response.headers['Authorization'] = f"Bearer {token}"
    return response


#註冊 --> 對比信箱及存入信箱、密碼及使用者名稱
@app.route('/register', methods=['POST'])
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
        user=session.query(User).filter(User.user_email==post_data.get('user_email')).first()
        if user is not None:
            response_object['status'] = "failure"
            response_object['message'] = "此信箱已被註冊過"
            return jsonify(response_object)

        new_user=User(user_email = post_data.get('user_email'),
                      user_password = hash_password(post_data.get('user_password')),
                      user_name = post_data.get('user_name'))
        session.add(new_user)
        session.commit()
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
