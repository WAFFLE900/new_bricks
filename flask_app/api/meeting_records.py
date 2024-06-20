from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import *
from sqlalchemy import exists, func, desc, and_
import logging
import json

bp = Blueprint('meeting_records', __name__)

# 回傳所有標籤
@bp.route('/tag_index', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def tag_index():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    project_id = post_data.get("project_id")
    user = GlobalObjects.flask_auth.current_user()

    project_exists = GlobalObjects.db_session.query(exists().where(Project.id == project_id)).scalar()
    if not project_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '專案不存在'
        return jsonify(response_object), 400
    
    try:
        id = post_data.get('project_id')
        result = (
            GlobalObjects.db_session.query(Tag.tag_class, func.group_concat(func.DISTINCT(Tag.tag_name)).label('tag_names'))
            .select_from(Project)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == id, Project.user_id == user.id)
            .group_by(Tag.tag_class)
            .distinct()
            .all()
        )
        print("result: ", result)
        sorted_tags = [{'tag_class': row.tag_class, 'tag_names': sorted(row.tag_names.split(','))} for row in result]
        response_object["item"] = sorted_tags
        response_object["message"] = "標籤回傳成功"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "標籤回傳失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400

# 標籤搜尋
@bp.route('/tag_search', methods=['POST'])
@GlobalObjects.flash_auth.login_required()
def tag_search():
    response_object = {'status': 'success'}
    try:
        post_data = request.get_json()
        id = post_data.get("project_id")
        user = GlobalObjects.flask_auth.current_user()

        project_exists = GlobalObjects.db_session.query(exists().where(Project.id == id)).scalar()
        if not project_exists:
            response_object['status'] = 'failed'
            response_object['message'] = '專案不存在'
            return jsonify(response_object), 400

        date_projects = (
            GlobalObjects.db_session.query(
                TextBox.id.label("TextBox_id"),
                TextBox.record_id,
                TextBox.textBox_content,
                func.concat(
                    '[',
                    func.group_concat(
                        func.concat(
                            '{"Tag_id": ', Tag.id, ', "Tag_name": "', Tag.tag_name, '", "Tag_class": "', Tag.tag_class, '"}'
                        )
                    ),
                    ']'
                ).label("Tag")
            )
            .select_from(User)
            .join(Project, User.id == Project.user_id)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == id, Project.user_id == user.id)
            .filter(Tag.tag_name.in_([tag_info["tag_name"] for tag_info in post_data.get("日期", [])]))
            .group_by(TextBox.id, TextBox.record_id, TextBox.textBox_content)
            .order_by(desc(func.count(Tag.id)))
            .all()
        )
        print("date_project: ", date_projects)

        undate_projects = (
            GlobalObjects.db_session.query(
                TextBox.id.label("TextBox_id"),
                TextBox.record_id,
                TextBox.textBox_content,
                func.concat(
                    '[',
                    func.group_concat(
                        func.concat(
                            '{"Tag_id": ', Tag.id, ', "Tag_name": "', Tag.tag_name, '", "Tag_class": "', Tag.tag_class, '"}'
                        )
                    ),
                    ']'
                ).label("Tag")
            )
            .select_from(User)
            .join(Project, User.id == Project.user_id)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == id)
            .filter(
                ~exists()
                .where(and_(
                        Tag.tag_class == '日期',
                        Tag.tag_name.in_([tag_info["tag_name"] for tag_info in post_data.get("日期", [])]),
                        TagTextBox.textBox_id == TextBox.id
                ))
                .correlate_except(TextBox)
            )
            .group_by(TextBox.id, TextBox.record_id, TextBox.textBox_content)
            .order_by(desc(func.count(Tag.id)))
            .all()
        )
        print("undate_project: ",undate_projects)

        response_object["item"] = {
            "match": [
                {
                    "TextBox_id": row[0],
                    "record_id": row[1],
                    "textBox_content": row[2],
                    "Tag": json.loads(f"[{row[3]}]")
                }
                for row in date_projects
            ],
            "unmatch": [
                {
                    "TextBox_id": row[0],
                    "record_id": row[1],
                    "textBox_content": row[2],
                    "Tag": json.loads(f"[{row[3]}]")
                }
                for row in undate_projects
                if row[0] not in [row[0] for row in date_projects]
            ]
        }
        response_object["message"] = "標籤回傳成功"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "標籤回傳失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400

# 新增標籤
@bp.route('/add_tag', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_tag():
    response_object = {"status": "success"}
    post_data = request.get_json()

    textbox_id=post_data.get("textBox_id")
    textbox_exists = GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id)).scalar()
    if not textbox_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '文字方框不存在'
        return jsonify(response_object), 400
    
    try:
        user = GlobalObjects.flask_auth.current_user()
        project_id = (
            GlobalObjects.db_session.query(Project.id)
            .select_from(User)
            .join(Project, User.id == Project.user_id)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .filter(TextBox.id == textbox_id)
            .filter(User.id == user.id)
            .scalar()
        )
        # 在porject_id已經篩過user_id了
        tag = (
            GlobalObjects.db_session.query(Tag)
            .select_from(Project)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == project_id)
            .filter(Tag.tag_name == post_data.get("tag_name"))
            .first()
        )
        if tag is None:
            print("tag is none")
            new_tag=Tag(tag_name=post_data.get("tag_name"), tag_class=post_data.get("tag_class"))
            GlobalObjects.db_session.add(new_tag)
            GlobalObjects.db_session.flush()
            GlobalObjects.db_session.commit()
            print("tag_name: ", post_data.get("tag_name"))
            new_tagId = (
                GlobalObjects.db_session.query(Tag.id)
                .filter(Tag.tag_name == post_data.get("tag_name"))
                .first()
            )
            print("new_tagId: ", new_tagId[0])
            new_tagTextBox=TagTextBox(tag_id=new_tagId[0], textBox_id=post_data.get("textBox_id"))
            GlobalObjects.db_session.add(new_tagTextBox)
            GlobalObjects.db_session.flush()
            GlobalObjects.db_session.commit()
            response_object["message"] = "新增{}成功".format(post_data.get("tag_name"))
        else:
            response_object["message"] = "標籤已存在"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)
    return jsonify(response_object)

# 刪除標籤
@bp.route('/delete_tag', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def delete_tag():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    try:
        tag_id = post_data.get("tag_id")
        dTag = GlobalObjects.db_session.query(Tag).filter(Tag.id==tag_id).first()
        print("tag to delete: ", dTag)
        if dTag is None:
            response_object["message"] = "標籤不存在"
        else:
            # 把所有table連起來判斷user_id
            project_id = (
                GlobalObjects.db_session.query(Project.id)
                .select_from(User)
                .join(Project, User.id == Project.user_id)
                .join(Record, Project.id == Record.project_id)
                .join(TextBox, Record.id == TextBox.record_id)
                .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
                .join(Tag, TagTextBox.tag_id == Tag.id)
                .filter(Tag.id == tag_id)
                .filter(User.id == user.id)
                .scalar()
            )
            if project_id is None:
                response_object['message'] = "user不擁有此標籤，無法刪除"
                return jsonify(response_object),403
            
            GlobalObjects.db_session.query(TagTextBox).filter(TagTextBox.tag_id == tag_id).delete()
            GlobalObjects.db_session.flush()
            GlobalObjects.db_session.query(Tag).filter(Tag.id==tag_id).delete()
            GlobalObjects.db_session.flush()
            GlobalObjects.db_session.commit()
            response_object["message"] = "刪除標籤{}成功".format(post_data.get("tag_id"))
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "標籤尋找失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),500
    return jsonify(response_object),400

# 刪除文字方塊
@bp.route('/delete_textBox', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def delete_texBox():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    textbox_id=post_data.get("textBox_id")
    textbox_exists = GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id)).scalar()
    if not textbox_exists:
        response_object['status'] = 'success'
        response_object['message'] = '文字方框不存在'
        return jsonify(response_object), 400
    
    try:
        user_owns_textBox = (
            GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id))
            .select_from(TextBox)
            .join(Record, TextBox.record_id == Record.id)
            .join(Project, Record.project_id == Project.id)
            .filter(Project.user_id == user.id)
            .scalar()
        )
        if not user_owns_textBox:
            response_object['message'] = 'user不擁有此文字方框，無法刪除'
            return jsonify(response_object), 403
        
        tag_textboxs= GlobalObjects.db_session.query(TagTextBox).filter_by(textBox_id=post_data.get("textBox_id")).all()
        if not tag_textboxs:
            response_object["message"] = "此文字方塊無標籤"
        else:
            tag_ids = [record.tag_id for record in tag_textboxs]
            # 提取 Tag 物件的 id 值
            tag_ids_to_delete = [tag.id for tag in GlobalObjects.db_session.query(Tag).filter(Tag.id.in_(tag_ids)).all()]
            # 查詢每個 tag_id 在 TagTextBox 中的引用次數
            tag_id_counts = (
                GlobalObjects.db_session.query(TagTextBox.tag_id, func.count())
                .filter(TagTextBox.tag_id.in_(tag_ids_to_delete))
                .group_by(TagTextBox.tag_id)
                .all()
            )
            print(tag_id_counts)
            for tag_id, count in tag_id_counts:
                GlobalObjects.db_session.query(TagTextBox).filter(TagTextBox.tag_id == tag_id, TagTextBox.textBox_id == post_data.get("textBox_id")).delete()
                GlobalObjects.db_session.flush()
                # 如果標籤只在要刪除的文字方塊中，刪除標籤
                if count == 1:
                    GlobalObjects.db_session.query(Tag).filter(Tag.id == tag_id).delete()
                    GlobalObjects.db_session.flush()
        GlobalObjects.db_session.query(TextBox).filter(TextBox.id == post_data.get("textBox_id")).delete()
        GlobalObjects.db_session.flush()
        GlobalObjects.db_session.commit()
        response_object["message"] = "刪除文字方框{}成功".format(post_data.get("textBox_id"))
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "文字方塊刪除失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400

# 顯示垃圾桶中會議記錄
@bp.route('/trashcan_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def trashcan_record():
    response_object = {'status': 'success'}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()
        data = (
            GlobalObjects.db_session.query(Record).filter(Record.project_id == post_data.get("project_id"), Record.record_trashcan==1, Record.user_id == user.id).all()
        )
        response_object["item"] = [{"Record.id": row.id, "Record.project_id": row.project_id} for row in data]
        response_object["message"] = "垃圾桶顯示成功"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "垃圾桶顯示失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)
    return jsonify(response_object)

@bp.route('/add_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_record():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    project_id = post_data.get("project_id")
    record_name=post_data.get("record_name")

    project_exists = GlobalObjects.db_session.query(exists().where(Project.id == project_id)).scalar()
    if not project_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '專案不存在'
        return jsonify(response_object), 400
    record_exists = GlobalObjects.db_session.query(exists().where(Record.record_name == record_name)).scalar()
    if record_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '會議記錄已存在'
        return jsonify(response_object), 400

    try:
        print(GlobalObjects.db_session.query(User).all())
        new_record = Record(record_name=post_data.get("record_name"),
                            record_date=post_data.get("record_date"),
                            record_department=post_data.get("record_department"),
                            # record_attendances=post_data.get("record_attendances"),
                            record_place=post_data.get("record_place"),
                            # record_host_name=post_data.get("record_host_name"),
                            record_trashcan=False,
                            user_id=user.id,
                            project_id=post_data.get("project_id"))
        GlobalObjects.db_session.add(new_record)
        GlobalObjects.db_session.flush()
        GlobalObjects.db_session.commit()
        print(new_record.id)

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 404
    response_object["message"] = "新增成功"
    response_object["record_id"] = new_record.id
    return jsonify(response_object),400

@bp.route('/get_record_index', methods=['POST'])
@GlobalObjects.flask_auth.login_required(optional=True)
def get_record_index():
    response_object = {'status': 'success'}
    user=GlobalObjects.flask_auth.current_user()
    post_data = request.get_json()
    try:
        response_object["record"] = []
        record_get = (
            GlobalObjects.db_session.query(Record)
            .join(Project, Record.project_id == Project.id)
            .filter(Project.user_id==user.id, Project.id == post_data.get("project_id"))
            .filter(Record.record_trashcan == False)
            .all()
        )
        print("user_id: ", user.id)
        print("record_get: ", record_get)
        for records in record_get:
            tag_get = GlobalObjects.db_session.query(Tag).join(TagTextBox, Tag.id == TagTextBox.tag_id).join(TextBox, TagTextBox.textBox_id == TextBox.id).join(Record, TextBox.record_id == Record.id).filter(TextBox.record_id == str(getattr(records, "id"))).all()
            
            return_tags = []
            for tags in tag_get:
                return_tags.append(str(getattr(tags, "tag_name")))

            response_object["record"].append({'record_name':str(getattr(records, "record_name")),
                                              'record_date':str(getattr(records, "record_date")),
                                              'record_department':str(getattr(records, "record_department")),
                                              #'record_attendances':str(getattr(records, "record_attendances")),
                                              'record_place':str(getattr(records, "record_place")),
                                              'record_attendees_name':str(getattr(records,"record_attendees_name")),
                                              #'record_host_name':str(getattr(records, "record_host_name")),
                                              'tags':return_tags
                                              })

    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)

    return jsonify(response_object),400

@bp.route('/edit_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def edit_record():
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    record_id=post_data.get("record_id")
    record_exists = GlobalObjects.db_session.query(exists().where(Record.id == record_id, Record.user_id==user.id)).scalar()
    if not record_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '會議記錄不存在'
        return jsonify(response_object), 400
    
    try:
        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id")).update({
            "record_name": post_data.get("record_name"),
            "record_department": post_data.get("record_department"),
            #"record_attendances": post_data.get("record_attendances"),
            "record_place": post_data.get("record_place")
        })
        GlobalObjects.db_session.commit()
        response_object["message"] = "修改成功"
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400

    return jsonify(response_object),400

@bp.route('/delete_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def delete_record():
    print("debug")
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    print("user_id",user.id)
    try:
        record_count = GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==user.id).count()
        if record_count == 0:
            response_object["status"] = "failed"
            response_object["message"] = "查無紀錄"
            return jsonify(response_object)
        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id")).update({"record_trashcan": 1})
        GlobalObjects.db_session.commit()
        response_object["message"] = "刪除成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400

    return jsonify(response_object),400

@bp.route('/get_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def get_record():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    try:        
        record_get = (
            GlobalObjects.db_session.query(Record)
            .join(Project, Record.project_id == Project.id)
            .filter(Project.id == post_data.get("project_id"))
            .filter(Project.user_id == user.id)
            .filter(Record.id == post_data.get("record_id"))
            .filter(Record.record_trashcan == 0)
        )
        record_data = row2dict(record_get)
        response_object["record_info"] = record_data
        textBox_list = []
        textBox_get = (
            GlobalObjects.db_session.query(TextBox)
            .join(Record, TextBox.record_id == Record.id)
            .filter(Record.id == post_data.get("record_id"))
            .filter(Record.record_trashcan == 0)
            .all()
        )
        textBox_data = row2dict(textBox_get)
        print(textBox_data)
        textBox_list.append(textBox_data)
        response_object["textBox"] = textBox_list
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)

    return jsonify(response_object)

@bp.route('/add_textBox', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_textBox():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    record_id=post_data.get("record_id")
    record_exists = GlobalObjects.db_session.query(exists().where(Record.id == record_id),Record.user_id==user.id).scalar()
    if not record_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '會議記錄不存在'
        return jsonify(response_object), 400
    
    try:        
        textBox = TextBox(textBox_content = post_data.get("textBox_content"),
                    record_id = post_data.get("record_id"))
        GlobalObjects.db_session.add(textBox)
        GlobalObjects.db_session.commit()
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)
    response_object["message"] = f"新增[{post_data.get('textBox_content')}] 進 record[{post_data.get('record_id')}]成功"
    return jsonify(response_object) ,400

@bp.route('/edit_textBox', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def edit_textBox():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    textbox_id=post_data.get("textBox_id")
    textbox_exists = GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id)).scalar()
    if not textbox_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '文字方框不存在'
        return jsonify(response_object), 400
    
    try:
        user_owns_textBox = (
            GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id))
            .select_from(TextBox)
            .join(Record, TextBox.record_id == Record.id)
            .join(Project, Record.project_id == Project.id)
            .filter(Project.user_id == user.id)
            .scalar()
        )
        if not user_owns_textBox:
            response_object['message'] = 'user不擁有此文字方框，無法編輯'
            return jsonify(response_object), 403
        else:
            GlobalObjects.db_session.query(TextBox).filter(TextBox.id == textbox_id).update({
                "textBox_content": post_data.get("textBox_content")
            })
            GlobalObjects.db_session.commit()
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    response_object["message"] = f"修改 textBox[{post_data.get('textBox_id')}] 的內容成[{post_data.get('textBox_content')}]成功"
    return jsonify(response_object),400

@bp.route('/recover_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def recover_record():
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    print("user.id",user.id)
    try:
        record_count = GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==user.id).count()
        if record_count == 0:
            response_object["status"] = "failed"
            response_object["message"] = "查無紀錄"
            return jsonify(response_object)
        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==post_data.get("user_id")).update({"record_trashcan":0})
        GlobalObjects.db_session.commit()
        response_object["message"] = "復原成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400

@bp.route('/delete_record_permanent', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def delete_record_permanent():
    response_object = {"status": "success"}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    try:
        record_count = GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==user.id).count()
        if record_count == 0:
            response_object["status"] = "failed"
            response_object["message"] = "查無紀錄"
            return jsonify(response_object)

        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==user.id).delete()
        GlobalObjects.db_session.commit()
        response_object["message"] = "刪除成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400

