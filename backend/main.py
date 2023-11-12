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

load_dotenv()

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')


app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})
app.config['SECRET_KEY'] = 'secret'

#連線到伺服器上的 MySQL
db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

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

    selectUserEmail = f""""
        SELECT user_email FROM users
        WHERE user_email = "{data['user_email']}";
    """
    ret = conn.execute(text(selectUserEmail))
    ret_list = ret.fetchall()
    if ret_list is None:
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
        selectUserId = f"""
            SELECT id, user_password FROM users
            WHERE user_email = "{post_data.get("user_email")}";
        """
        result = conn.execute(text(selectUserId))
        result_list = result.fetchall()
        response_object['user_id'] = result_list[0][0]
        user_password = result_list[0][1]
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
    result.close()
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
        isRegisted = f"""
            SELECT IF(SUM(IF(user_email != "{post_data.get("user_email")}", 0, 1))>0, 1, 0) AS exist FROM users;
        """
        result = conn.execute(text(isRegisted))
        result_list = result.fetchall()
        if (result_list[0][0] == 0):
            hashed_password = hash_password(post_data.get("user_password"))
            addAccount = f"""
            INSERT INTO users (user_email, user_password, user_name)
            VALUES ("{post_data.get("user_email")}", "{hashed_password}"," {post_data.get("user_name")}");
            """
            print(hashed_password)
            conn.execute(text(addAccount))
            conn.execute(text("COMMIT;"))
        else:
            response_object['status'] = "failure"
            response_object['message'] = "此信箱已被註冊過"
            return jsonify(response_object)

        selectUserId = f"""
            SELECT id FROM users
            WHERE user_email = "{post_data.get("user_email")}";
        """
        result2 = conn.execute(text(selectUserId))
        result2_list = result2.fetchall()
        response_object['user_id'] = result2_list[0][0]

    except:
        response_object['status'] = "failure"
        response_object['message'] = "SELECT user_id 失敗 或 INSERT 失敗"
        return jsonify(response_object)

    result.close()
    result2.close()
    conn.close()
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
        addInfo = f"""
            UPDATE users
            SET user_purpose = "{",".join(post_data.get("user_purpose"))}", user_identity = "{(post_data.get("user_identity"))}", user_otherTool = "{",".join(post_data.get("user_otherTool"))}" 
            WHERE id = {(post_data.get("user_id"))};
        """
        conn.execute(text(addInfo))
        conn.execute(text("COMMIT;"))

        selectId = f"""
            SELECT user_email FROM users
            WHERE id = {(post_data.get("user_id"))};
        """
        result = conn.execute(text(selectId))
        response_object['user_email'] = result.fetchall()[0][0]

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
        nor_query = """
                    SELECT p.project_id, p.project_image,p.project_name,p.project_creation_date,p.edit_date,p.user_id
                    FROM project p
                    JOIN project_sort ps ON p.project_type = ps.project_type
                    WHERE p.user_id = {}
                    AND p.project_trashcan = 0
                    AND p.project_ended = 0
                    AND ps.user_id = {}
                    ORDER BY ps.project_type_sort ASC, p.project_edit_date DESC;
                """.format(post_data.get("user_id"), post_data.get("user_id"))
        SQL_data = conn.execute(text(nor_query))
        keys = list(SQL_data.keys())
        data = [dict(zip(keys, row)) for row in SQL_data.fetchall()]
        conn.close()
        response_object["items"] = dict()
        for row in data:
            project_type = row.pop("project_type")
            if project_type not in response_object["items"]:
                response_object["items"][project_type] = list()
                response_object["items"][project_type].append(row)
        found = True                     
        conn.close()

    if post_data.get("project_status") == "ended":
        end_query = """
                    SELECT p.project_id, p.project_image,p.project_name,p.project_creation_date,p.edit_date,p.user_id
                    FROM project p
                    JOIN project_sort ps ON p.project_type = ps.project_type
                    WHERE p.user_id = {}
                    AND p.project_trashcan = 0
                    AND p.project_ended = 1
                    AND ps.user_id = {}
                    ORDER BY ps.project_type_sort ASC, p.project_edit_date DESC;
                """.format(post_data.get("user_id"), post_data.get("user_id"))
        SQL_data = conn.execute(text(end_query))
        keys = list(SQL_data.keys())
        data = [dict(zip(keys, row)) for row in SQL_data.fetchall()]
        found = True
        response_object["items"] = dict()
        for row in data:
            project_type = row.pop("project_type")
            if project_type not in response_object["items"]:
                response_object["items"][project_type] = list()
                response_object["items"][project_type].append(row)
        conn.close()


    if post_data.get("project_status") == "trashcan":
        month_query = """
                    SELECT p.project_id, p.project_image,p.project_name,p.project_creation_date,p.edit_date,p.user_id
                    FROM project
                    WHERE user_id = {} AND project_trashcan = 1
                        AND project_edit_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    ORDER BY project_edit_date DESC;
                """.format(post_data.get("user_id"))
        not_month_query = """
                    SELECT p.project_id, p.project_image,p.project_name,p.project_creation_date,p.edit_date,p.user_id
                    FROM project
                    WHERE user_id = {} AND project_trashcan = 1
                        AND project_edit_date < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    ORDER BY project_edit_date DESC;
        """.format(post_data.get("user_id"))

        month = conn.execute(text(month_query))
        keys = list(month.keys())
        month_data = [dict(zip(keys, row)) for row in month.fetchall()]

        not_month = conn.execute(text(not_month_query))
        keys = list(not_month.keys())
        not_month_data = [dict(zip(keys, row)) for row in not_month.fetchall()]

        found = True
        response_object["month"] = dict()
        for row in month_data:
            project_type = row.pop("project_type")
            if project_type not in response_object["items"]:
                response_object["items"][project_type] = list()
                response_object["items"][project_type].append(row)
        response_object["not_in_month"] = dict()
        for row in not_month_data:
            project_type = row.pop("project_type")
            if project_type not in response_object["items"]:
                response_object["items"][project_type] = list()
                response_object["items"][project_type].append(row)
        conn.close()
        response_object["message"] = "垃圾桶"
    
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
        set_query = """
                        UPDATE project SET project_ended = 1 WHERE id = {};
                    """.format(post_data.get("project_id"))
        conn.execute(text(set_query))
        conn.execute(text("COMMIT;"))
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



        Inquery = """
            INSERT INTO project (project_type, project_image, project_name, project_trashcan, project_ended, project_edit, project_visible, project_comment, user_id)
            VALUES 
            ("{}", "{}", "{}", {}, {}, {}, {}, {}, {});
        """.format(post_data.get("project_type"), post_data.get("project_image"), post_data.get("project_name"), post_data.get("project_trashcan"), post_data.get("project_ended"), 
                post_data.get("project_isEdit"), post_data.get("project_isVisible"), post_data.get("project_isComment"), post_data.get("user_id"))


        #執行SQL指令
        conn.execute(text(Inquery))
        conn.execute(text("COMMIT;"))
        #關閉連線
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

        get_last_query = """
                    SELECT MAX(project_type_sort) AS max_sort FROM project_sort
                    WHERE user_id = {} AND project_ended = {};
        """.format(post_data.get("user_id"), post_data.get("project_ended"))

        last = conn.execute(text(get_last_query))
        keys = list(last.keys())
        last = [dict(zip(keys, row)) for row in last.fetchall()]

        get_last_id_query = """
                    SELECT MAX(type_id) AS max_sort FROM project_sort
                    WHERE user_id = {} AND project_ended = {};
        """.format(post_data.get("user_id"), post_data.get("project_ended"))

        last_id = conn.execute(text(get_last_id_query))
        keys = list(last_id.keys())
        last_id = [dict(zip(keys, row)) for row in last_id.fetchall()]

        sort = last[0]["max_sort"] + 1
        id = last_id[0]["max_sort"] + 1

        Inquery = """
            INSERT INTO project_sort (type_id, project_type, project_type_sort, user_id, project_ended)
            VALUES 
            ({}, "{}", {}, {}, {});
        """.format(id, post_data.get("project_type"), sort, post_data.get("user_id"), post_data.get("project_ended"))

        #執行SQL指令
        conn.execute(text(Inquery))
        conn.execute(text("COMMIT;"))
        #關閉連線
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
        set_query = """
                        UPDATE project SET project_type = '{}' WHERE id = {};
                    """.format(post_data.get("project_type"), post_data.get("project_id"))
        conn.execute(text(set_query))
        conn.execute(text("COMMIT;"))
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
        set_query = """
                        UPDATE project SET project_trashcan = 0
                        WHERE id = {};
                    """.format(post_data.get("project_id"))
        conn.execute(text(set_query))
        conn.execute(text("COMMIT;"))
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
            requery = """
            UPDATE project_sort SET project_type_sort = {} WHERE type_id = {} AND user_id = {} AND project_ended = {};
            """.format(project_type_sort, id, post_data.get("user_id"), post_data.get("project_ended"))
            conn.execute(text(requery))
            print("sort:{}, type_id:{}, user_id:{}".format(project_type_sort, id, post_data.get("user_id")))
        conn.execute(text("COMMIT;"))
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
        set_query = """
                        UPDATE project SET project_trashcan = 1
                        WHERE id = {};
                    """.format(post_data.get("project_id"))
        conn.execute(text(set_query))
        conn.execute(text("COMMIT;"))
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
        
        nor_query = """
                        SELECT id, user_avatar, user_email, user_identity, user_name, user_otherTool, user_password, user_purpose
                        FROM users WHERE id = {};
                    """.format(post_data.get("user_id"))
        SQL_data = conn.execute(text(nor_query))
        keys = list(SQL_data.keys())
        data = [dict(zip(keys, row)) for row in SQL_data.fetchall()]
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
        notificationInfo = f"""SELECT id, notification_content, notification_id, notification_isRead, notification_recipient_id, notification_sender_id
        FROM notification
        JOIN mention
        ON notification.id=mention.notification_id
        WHERE mention.notification_recipient_id={user_id};"""

        result = conn.execute(text(notificationInfo))
        cols = list(result.keys())
        data = [dict(zip(cols, row)) for row in result.fetchall()]

        response_object['items'] = data
    except:
        response_object['status'] = "algorithm failure"

    result.close()
    conn.close()
    return jsonify(response_object)


@app.route('/search_history', methods=['POST'])
def search_history():
    response_object = {'status': 'success'}
    try:
        conn = engine.connect()
    except:
        response_object['status'] = "connect failure"
    user_id = request.get_json().get("user_id")
    try:
        historySort = f"""
        SELECT id, user_id, search_content, search_time
        FROM search_history
        WHERE user_id={user_id}
        ORDER BY search_time DESC
        LIMIT 3;
        """
        result = conn.execute(text(historySort))
        cols = list(result.keys())
        data = [dict(zip(cols, row)) for row in result.fetchall()]
        response_object['items'] = data
    except:
        response_object['status'] = "history fetch failure"
    result.close()
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
    user_id = request.get_json().get("user_id")
    try:
        isSame = f"""
        SELECT COUNT(*) FROM search_history
        WHERE user_id={user_id} AND search_content="{search_content}" """
        result1 = conn.execute(text(isSame))
        is_same = result1.fetchall()[0][0]

        if is_same == 0:
            nextID = f"""SELECT COUNT(*)+1 FROM search_history"""
            result2 = conn.execute(text(nextID))
            next_id = result2.fetchall()[0][0]
            historyWrite = f"""
            INSERT INTO search_history (id,user_id,search_content,search_time)
            VALUES ({next_id},{user_id},"{search_content}",NOW())
            """
            result2.close()
        else:
            historyWrite = f"""
            UPDATE search_history
            SET search_time=NOW()
            WHERE user_id={user_id} AND search_content="{search_content}";
            """
        conn.execute(text(historyWrite))
        conn.execute(text("COMMIT;"))
    except:
        response_object['status'] = "history insert failure"

    S_DATA = []
    try:
        searchResult = f"""SELECT * FROM project WHERE user_id={user_id};"""

        result = conn.execute(text(searchResult))
        cols = list(result.keys())
        data = [dict(zip(cols, row)) for row in result.fetchall()]

        for project_info in data:
            if lcs(project_info) > 0:
                S_DATA.append(project_info)

        S_DATA.sort(key=lcs, reverse=True)

        response_object['items'] = S_DATA
    except:
        response_object['status'] = "algorithm failure"

    result.close()
    result1.close()
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
