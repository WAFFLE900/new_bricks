from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import *
from flask_app.auth import make_JWT, hash_password
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz

bp = Blueprint('user_homepage', __name__)

@bp.route('/project_index', methods=['POST'])
@GlobalObjects.flask_auth.login_required(optional=True)
def get_project():
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    # def get_data(sql):
    #     data = {}
    #     for project, project_sort in sql:
    #         d = {}
    #         for column in project.__table__.columns:
    #             d[column.name] = str(getattr(project, column.name))
    #         del d['project_type']
    #         d['type_id'] = project_sort.type_id
    #         if project.project_type not in data.keys():
    #             data[project.project_type] = []
    #         data[project.project_type].append(d)
    #     return data
    if post_data.get("project_status") == "normal":
        try:
            SQL_q_item = GlobalObjects.db_session.query(
                Project
            ).filter(
                Project.user_id==user.id,
                Project.project_trashcan==0,
                Project.project_ended==0
            ).order_by(
                Project.project_edit_date.desc()
            ).all()

            SQL_q_user = GlobalObjects.db_session.query(
                User
            ).filter(
                User.id==user.id,
            ).all()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            GlobalObjects.db_session.rollback()
            return jsonify(response_object), 404
        data = row2dict(SQL_q_item)
        username = row2dict(SQL_q_user)
        response_object["items"] = [{
            'id': data[i]['id'],
            'project_comment': data[i]['project_comment'],
            'project_edit_date': data[i]['project_edit_date'],
            'project_image': data[i]['project_image'],
            'project_name': data[i]['project_name'],
            'project_type': data[i]['project_type'],
            'user_id': data[i]['user_id']
        }
        for i in range(len(data))
        ]
        response_object["user_name"] = [{
            'user_name': username[i]['user_name']
        }
        for i in range(len(username))
        ]
        response_object["message"] = "正在進行專案"

    elif post_data.get("project_status") == "ended":
        try:
            SQL_q_item = GlobalObjects.db_session.query(
                Project
            ).filter(
                Project.user_id==user.id,
                Project.project_trashcan==0,
                Project.project_ended==1
            ).order_by(
                Project.project_edit_date.desc()
            ).all()

            SQL_q_user = GlobalObjects.db_session.query(
                User
            ).filter(
                User.id==user.id,
            ).all()
        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            GlobalObjects.db_session.rollback()
            return jsonify(response_object), 404
        data = row2dict(SQL_q_item)
        username = row2dict(SQL_q_user)
        response_object["items"] = [{
            'id': data[i]['id'],
            'project_comment': data[i]['project_comment'],
            'project_edit_date': data[i]['project_edit_date'],
            'project_image': data[i]['project_image'],
            'project_name': data[i]['project_name'],
            'project_type': data[i]['project_type'],
            'user_id': data[i]['user_id']
        }
        for i in range(len(data))
        ]
        response_object["user_name"] = [{
            'user_name': username[i]['user_name']
        }
        for i in range(len(username))
        ]
        response_object["message"] = "已結束專案"

    elif post_data.get("project_status") == "trashcan":
        try:
            time_delta = datetime.now() - relativedelta(months=1)
            in_month_SQL_data = GlobalObjects.db_session.query(
                Project
            ).filter(
                Project.user_id == user.id,
                Project.project_trashcan == 1,
                Project.project_edit_date>=time_delta
            ).order_by(
                Project.project_edit_date.desc()
            ).all()

            not_in_month_SQL_data = GlobalObjects.db_session.query(
                Project
            ).filter(
                Project.user_id == user.id,
                Project.project_trashcan == 1,
                Project.project_edit_date<time_delta
            ).order_by(
                Project.project_edit_date.desc()
            ).all()

            SQL_q_user = GlobalObjects.db_session.query(
                User
            ).filter(
                User.id==user.id,
            ).all()

        except Exception as e:
            response_object["status"] = "failed"
            response_object["message"] = "SQL 搜尋失敗"
            print(str(e))
            GlobalObjects.db_session.rollback()
            return jsonify(response_object), 404
        # print(in_month_SQL_data)
        in_month_data = row2dict(in_month_SQL_data)
        not_in_month_data = row2dict(not_in_month_SQL_data)
        username = row2dict(SQL_q_user)
        response_object["item"] = {
            "in_month": [{
                        'id': in_month_data[i]['id'],
                        'project_comment': in_month_data[i]['project_comment'],
                        'project_edit_date': in_month_data[i]['project_edit_date'],
                        'project_image': in_month_data[i]['project_image'],
                        'project_name': in_month_data[i]['project_name'],
                        'project_type': in_month_data[i]['project_type'],
                        'user_id': in_month_data[i]['user_id']
                    }
                    for i in range(len(in_month_data))
                    ],
            "not_int_month":[{
                        'id': not_in_month_data[i]['id'],
                        'project_comment': not_in_month_data[i]['project_comment'],
                        'project_edit_date': not_in_month_data[i]['project_edit_date'],
                        'project_image': not_in_month_data[i]['project_image'],
                        'project_name': not_in_month_data[i]['project_name'],
                        'project_type': not_in_month_data[i]['project_type'],
                        'user_id': not_in_month_data[i]['user_id']
                    }
                    for i in range(len(not_in_month_data))
                    ],
        }
        response_object["user_name"] = [{
            'user_name': username[i]['user_name']
        }
        for i in range(len(username))
        ]
        response_object["message"] = "垃圾桶"

    return jsonify(response_object)


@bp.route("/set_project_end", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def set_end():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        if(post_data.get("state") == "end"):
            state = True
        elif(post_data.get("state") == "open"):
            state = False
        GlobalObjects.db_session.query(Project).filter(Project.id==post_data.get("project_id")).update({"project_ended":state})
        GlobalObjects.db_session.commit()
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "SQL 搜尋失敗，找不到專案"
        print(str(e))
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 404
    response_object["message"] = "修改成功"
    return jsonify(response_object)


@bp.route('/add_project', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_project():
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    try:
        print(GlobalObjects.db_session.query(User).all())
        new_project = Project(project_type=post_data.get("project_type"), project_image=post_data.get("project_image"),
                            project_name=post_data.get("project_name"), project_trashcan=post_data.get("project_trashcan"),
                            project_ended=post_data.get("project_ended"), project_edit=post_data.get("project_isEdit"),
                            project_visible=post_data.get("project_isVisible"), project_comment=post_data.get("project_isComment"),
                            user_id=user.id)
        GlobalObjects.db_session.add(new_project)
        GlobalObjects.db_session.flush()
        GlobalObjects.db_session.commit()
        print(new_project.id)

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        GlobalObjects.db_session.rollback()
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 404
    response_object["message"] = "新增{}成功".format(post_data.get("project_name"))
    return jsonify(response_object)



@bp.route("/add_type", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def add_type():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        GlobalObjects.db_session.query(Project).filter(Project.id==post_data.get("project_id")).update({"project_type":post_data.get("project_type")})
        GlobalObjects.db_session.commit()

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        GlobalObjects.db_session.rollback()
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 404
    response_object["message"] = "新增{}成功".format(post_data.get("project_type"))
    return jsonify(response_object)


@bp.route("/edit_type", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def set_type():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        project_count = GlobalObjects.db_session.query(Project).filter(Project.project_type == post_data.get("old_project_type")).count()
        if project_count == 0:
            response_object["status"] = "failed"
            response_object["message"] = "輸入類別名稱錯誤"
            return jsonify(response_object)
        if post_data.get("project_type") == None:
            response_object["message"] = "類別名稱未修改"
            return jsonify(response_object)
        GlobalObjects.db_session.query(Project).filter(Project.project_type == post_data.get("old_project_type")).update({"project_type": post_data.get("project_type")})
        GlobalObjects.db_session.commit()
        response_object["message"] = f"{post_data.get('old_project_type')}成功修改成{post_data.get('project_type')}"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        print(e)
        GlobalObjects.db_session.rollback()


@bp.route("/to_trashcan", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def trashcan():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user().id
        project=GlobalObjects.db_session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=1
        GlobalObjects.db_session.commit()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()

    return jsonify(response_object)


@bp.route("/trashcan_recover", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def recover():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        project=GlobalObjects.db_session.query(Project).filter(Project.id==post_data.get("project_id")).first()
        if project is None:
            response_object["status"]="failed"
            response_object["message"]="找不到專案"
            return jsonify(response_object)
        project.project_trashcan=0
        GlobalObjects.db_session.commit()
        response_object["message"] = "修改成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()

    return jsonify(response_object)


@bp.route("/permanent_delete", methods=["POST"])
@GlobalObjects.flask_auth.login_required()
def permanent_delete():
    response_object = {"status": "success"}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        GlobalObjects.db_session.query(Project).filter(Project.id==post_data.get("project_id")).delete()
        GlobalObjects.db_session.flush()
        GlobalObjects.db_session.commit()
        response_object["message"] = "永久刪除成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()

    return jsonify(response_object)


@bp.route('/search', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def search():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    try:
        rank_score = []
        status = post_data.get("search_status")
        if status == "normal":
            project_list = GlobalObjects.db_session.query(Project).filter(Project.user_id == user.id, Project.project_ended == False, Project.project_trashcan == False).all()
        elif status == "ended":
            project_list = GlobalObjects.db_session.query(Project).filter(Project.user_id == user.id, Project.project_ended == True, Project.project_trashcan == False).all()
        elif status == "trashcan":
            project_list = GlobalObjects.db_session.query(Project).filter(Project.user_id == user.id, Project.project_trashcan == True).all()
        elif status == "":
            project_list = GlobalObjects.db_session.query(Project).filter(Project.user_id == user.id).all()

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
        GlobalObjects.db_session.rollback()

    response_object['items'] = sorted_rank
    return jsonify(response_object)