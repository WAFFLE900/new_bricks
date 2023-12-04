# app/modules/file_module.py
from flask import Blueprint
from . import *

personal_page_module = Blueprint("personal_page_module", __name__)

def row2dict(SQL_data):    
    data = []
    for row in SQL_data:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        data.append(d)
    return data

@personal_page_module.route('/project_index', methods=['POST'])
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


@personal_page_module.route("/set_project_end", methods=["POST"])
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

@personal_page_module.route('/add_project', methods=['POST'])
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


@personal_page_module.route("/add_type", methods=["POST"])
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

@personal_page_module.route("/edit_type", methods=["POST"])
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


@personal_page_module.route("/trashcan_recover", methods=["POST"])
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

@personal_page_module.route("/to_trashcan", methods=["POST"])
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

@personal_page_module.route('/search', methods=['POST'])
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

#-----------------------------------------------------------------------------------------------------------------------------------------

# # 還沒改
# @personal_page_module.route("/personal_setting", methods=["POST"])
# def personal_setting():
#     try:
#         conn = engine.connect()
#         response_object = {"status": "success"}
#         post_data = request.get_json()
        
#         nor_query = """
#                         SELECT id, user_avatar, user_email, user_identity, user_name, user_otherTool, user_password, user_purpose
#                         FROM users WHERE id = {};
#                     """.format(post_data.get("user_id"))
#         SQL_data = conn.execute(text(nor_query))
#         keys = list(SQL_data.keys())
#         data = [dict(zip(keys, row)) for row in SQL_data.fetchall()]
#         conn.close()
#         response_object["items"] = data
    
#     except Exception as e:
#         response_object["status"] = "failed"
#         response_object["message"] = str(e)

#     return jsonify(response_object)

# # 還沒改
# @personal_page_module.route('/notification', methods=['POST'])
# def notification():
#     response_object = {'status': 'success'}
#     try:
#         conn = engine.connect()
#     except:
#         response_object['status'] = "connect failure"
#     user_id = request.get_json().get("user_id")
#     try:
#         notificationInfo = f"""SELECT id, notification_content, notification_id, notification_isRead, notification_recipient_id, notification_sender_id
#         FROM notification
#         JOIN mention
#         ON notification.id=mention.notification_id
#         WHERE mention.notification_recipient_id={user_id};"""

#         result = conn.execute(text(notificationInfo))
#         cols = list(result.keys())
#         data = [dict(zip(cols, row)) for row in result.fetchall()]

#         response_object['items'] = data
#     except:
#         response_object['status'] = "algorithm failure"

#     result.close()
#     conn.close()
#     return jsonify(response_object)


# @personal_page_module.route('/search_history', methods=['POST'])
# def search_history():
#     response_object = {'status': 'success'}
#     try:
#         conn = engine.connect()
#     except:
#         response_object['status'] = "connect failure"
#     user_id = request.get_json().get("user_id")
#     try:
#         historySort = f"""
#         SELECT id, user_id, search_content, search_time
#         FROM search_history
#         WHERE user_id={user_id}
#         ORDER BY search_time DESC
#         LIMIT 3;
#         """
#         result = conn.execute(text(historySort))
#         cols = list(result.keys())
#         data = [dict(zip(cols, row)) for row in result.fetchall()]
#         response_object['items'] = data
#     except:
#         response_object['status'] = "history fetch failure"
#     result.close()
#     conn.close()
#     return jsonify(response_object)

# # 沒有用了
# @personal_page_module.route("/type_reindex", methods=["POST"])
# def type_reindex():
#     response_object = {"status": "success"}
#     try:
#         post_data = request.get_json()
        
#         for item in post_data.get("type_sort"):
#             id = item["id"]
#             project_type_sort = item["project_type_sort"]
#             requery = """
#             UPDATE project_sort SET project_type_sort = {} WHERE type_id = {} AND user_id = {} AND project_ended = {};
#             """.format(project_type_sort, id, post_data.get("user_id"), post_data.get("project_ended"))
#             conn.execute(text(requery))
#             print("sort:{}, type_id:{}, user_id:{}".format(project_type_sort, id, post_data.get("user_id")))
#         session.commit()
#         response_object["message"] = "修改成功"

#     except Exception as e:
#         response_object["status"] = "failed"
#         response_object["message"] = str(e)

#     return jsonify(response_object)

# # 解除已結束專案狀態
# @personal_page_module.route("/return_project_end", methods=["POST"])
# def return_end():
#     response_object = {"status": "success"}
#     try:
#         post_data = request.get_json()
#         session.query(Project).filter(Project.id==post_data.get("project_id")).update({"project_ended":False})
#         session.commit()
#     except Exception as e:
#         response_object["status"] = "failed"
#         response_object["message"] = "SQL 搜尋失敗，找不到專案"
#         print(str(e))
#         return jsonify(response_object), 404
#     response_object["message"] = "解除已結束專案狀態"
#     return jsonify(response_object)
