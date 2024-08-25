from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import *
from sqlalchemy import exists, func, desc, and_
import logging
import json
import re
from datetime import datetime, timezone, timedelta

bp = Blueprint('meeting_records', __name__)

# 列出所有會議紀錄
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
            .order_by(desc(Record.record_creation_time))
            .all()
        )
        print("user_id: ", user.id)
        print("record_get: ", record_get)
        for records in record_get:
            tag_get = (GlobalObjects.db_session.query(Tag)
                       .join(TagTextBox, Tag.id == TagTextBox.tag_id)
                       .join(TextBox, TagTextBox.textBox_id == TextBox.id)
                       .join(Record, TextBox.record_id == Record.id)
                       .filter(TextBox.record_id == str(getattr(records, "id")))
                       .all()
                    )
            
            return_tags = []
            for tags in tag_get:
                return_tags.append(str(getattr(tags, "tag_name")))

            response_object["record"].append({  'record_id':str(getattr(records, "id")),
                                                'record_name':str(getattr(records, "record_name")),
                                            #   'record_date':str(getattr(records, "record_date")),
                                            #   'record_department':str(getattr(records, "record_department")),
                                            #   'record_attendances':str(getattr(records, "record_attendances")),
                                            #   'record_place':str(getattr(records, "record_place")),
                                            #   'record_attendees_name':str(getattr(records,"record_attendees_name")),
                                            #   'record_host_name':str(getattr(records, "record_host_name")),
                                                'tags':return_tags
                                              })

    except Exception as e:
        print(e)
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)

    return jsonify(response_object),200

# 顯示會議記錄資訊
@bp.route('/get_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def get_record():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    record_id=post_data.get("record_id")
    project_id=post_data.get("project_id")
    record_exists = GlobalObjects.db_session.query(exists().where(Record.id == record_id, Record.project_id==project_id, Record.user_id==user.id)).scalar()
    if not record_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '會議記錄不存在'
        return jsonify(response_object), 400

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
        textBox_get = (
            GlobalObjects.db_session.query(
                TextBox.id, TextBox.record_id, TextBox.textBox_content, TextBox.textBox_update_time,
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
            .select_from(Record)
            .join(TextBox, Record.id == TextBox.record_id)
            .outerjoin(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .outerjoin(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Record.id == post_data.get("record_id"))
            .filter(Record.record_trashcan == 0)
            .group_by(TextBox.id, TextBox.record_id, TextBox.textBox_content, TextBox.textBox_update_time) # group by all the non-aggregated columes
            .order_by(Record.id)
            .all()
        )
        for row in textBox_get:
            print(row)
        response_object["textBox"] = [
            {
                "TextBox_id": row[0],
                "record_id": row[1],
                "textBox_content": row[2],
                "textBox_update_time": row[3],
                "Tag": (lambda x:json.loads(f"{x}") if x is not None else None)(row[4])
            }
            for row in textBox_get
        ]
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)

    return jsonify(response_object)

# 新增會議紀錄
@bp.route('/add_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_record():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    project_id = post_data.get("project_id")
    # record_name=post_data.get("record_name")

    project_exists = GlobalObjects.db_session.query(exists().where(Project.id == project_id, Project.user_id == user.id)).scalar()
    if not project_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '專案不存在'
        return jsonify(response_object), 400
    # record_exists = GlobalObjects.db_session.query(exists().where(Record.record_name == record_name)).scalar()
    # if record_exists:
    #     response_object['status'] = 'failed'
    #     response_object['message'] = '會議記錄已存在'
    #     return jsonify(response_object), 400

    unamed_records = (GlobalObjects.db_session.query(Record.record_name)
                      .join(Project, Record.project_id == Project.id)
                      .filter(Project.user_id == user.id)
                      .filter(Record.project_id == project_id)
                      .filter(Record.record_name.like('未命名會議紀錄%'))
                      .all()
                    )
    print(unamed_records)
    pattern = re.compile(r'^未命名會議紀錄(\d+)$')
    max_unamed_record_index = max(
            [int(pattern.match(record_name[0]).group(1)) for record_name in unamed_records if pattern.match(record_name[0])],
            default=0
        )
    # return {'max_idx': max_unamed_record_index}, 400

    try:
        print(GlobalObjects.db_session.query(User).all())
        new_record = Record(record_name=f'未命名會議紀錄{max_unamed_record_index + 1}',
                            record_date=post_data.get("record_date"),
                            # record_department=post_data.get("record_department"),
                            # record_attendances=post_data.get("record_attendances"),
                            # record_place=post_data.get("record_place"),
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
    response_object["record_name"] = new_record.record_name
    return jsonify(response_object),200

# 修改會議記錄
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
            # "record_department": post_data.get("record_department"),
            #"record_attendances": post_data.get("record_attendances"),
            "record_attendees_name": post_data.get("record_attendees_name"),
            "record_absentees_name": post_data.get("record_absentees_name"),
            "record_recorder_name": post_data.get("record_recorder_name"),
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

    return jsonify(response_object),200

# 刪除會議記錄(丟入垃圾桶)
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
            return jsonify(response_object),400
        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id")).update({"record_trashcan": 1})
        GlobalObjects.db_session.commit()
        response_object["message"] = "刪除成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400

    return jsonify(response_object),200

# 復原會議記錄
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
            return jsonify(response_object),400
        GlobalObjects.db_session.query(Record).filter(Record.id == post_data.get("record_id"),Record.user_id==user.id).update({"record_trashcan":0})
        GlobalObjects.db_session.commit()
        response_object["message"] = "復原成功"

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),200

# 永久刪除會議紀錄
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
    return jsonify(response_object),200

# 新增文字方塊
@bp.route('/add_textBox', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def add_textBox():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()

    record_id=post_data.get("record_id")
    record_exists = GlobalObjects.db_session.query(exists().where(Record.id == record_id,Record.user_id==user.id)).scalar()
    if not record_exists:
        response_object['status'] = 'failed'
        response_object['message'] = '會議記錄不存在'
        return jsonify(response_object), 400
    
    try:        
        textBox = TextBox(textBox_content = post_data.get("textBox_content"),
                    record_id = post_data.get("record_id"))
        GlobalObjects.db_session.add(textBox)
        GlobalObjects.db_session.commit()
        GlobalObjects.db_session.query(Record).filter(Record.id == record_id,Record.user_id==user.id).update({
            'record_update_time': textBox.textBox_update_time
        })
        GlobalObjects.db_session.commit()
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 400
    response_object["message"] = f"新增[{post_data.get('textBox_content')}] 進 record[{post_data.get('record_id')}]成功"
    return jsonify(response_object) ,200

# 修改文字方塊
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
        # user_owns_textBox = (
        #     GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id))
        #     .select_from(TextBox)
        #     .join(Record, TextBox.record_id == Record.id)
        #     .join(Project, Record.project_id == Project.id)
        #     .filter(Project.user_id == user.id)
        #     .scalar()
        # )

        user_owns_textBox = (
            GlobalObjects.db_session.query(
                GlobalObjects.db_session.query(TextBox.id)
                .join(Record, TextBox.record_id == Record.id)
                .join(Project, Record.project_id == Project.id)
                .filter(TextBox.id == textbox_id, Project.user_id == user.id)
                .exists()
            )
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
            textBox = GlobalObjects.db_session.query(TextBox).filter(TextBox.id == textbox_id).first()
            GlobalObjects.db_session.query(Record).filter(Record.id == textBox.record_id, Record.user_id==user.id).update({
                'record_update_time': textBox.textBox_update_time
            })
            GlobalObjects.db_session.commit()
    except Exception as e:
        print(str(e))
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    response_object["message"] = f"修改 textBox[{post_data.get('textBox_id')}] 的內容成[{post_data.get('textBox_content')}]成功"
    return jsonify(response_object),200

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
        # user_owns_textBox = (
        #     GlobalObjects.db_session.query(exists().where(TextBox.id == textbox_id))
        #     .select_from(TextBox)
        #     .join(Record, TextBox.record_id == Record.id)
        #     .join(Project, Record.project_id == Project.id)
        #     .filter(Project.user_id == user.id)
        #     .scalar()
        # )

        user_owns_textBox = (
            GlobalObjects.db_session.query(
                GlobalObjects.db_session.query(TextBox.id)
                .join(Record, TextBox.record_id == Record.id)
                .join(Project, Record.project_id == Project.id)
                .filter(TextBox.id == textbox_id, Project.user_id == user.id)
                # .filter(TextBox.id == textbox_id, Project.user_id == 34)
                .exists()
            )
            .scalar()
        )

        if not user_owns_textBox:
            response_object['message'] = 'user不擁有此文字方框，無法刪除'
            return jsonify(response_object), 403
        
        record_id = (
            GlobalObjects.db_session.query(Record.id)
            .join(TextBox, Record.id == TextBox.record_id)
            .filter(TextBox.id == textbox_id)
            .scalar()
        )

        tag_textboxs= GlobalObjects.db_session.query(TagTextBox).filter_by(textBox_id=post_data.get("textBox_id")).all()
        if not tag_textboxs:
            response_object["message"] = "此文字方塊無標籤"
            print("此文字方塊無標籤")
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

        GlobalObjects.db_session.query(Record).filter(Record.id == record_id, Record.user_id==user.id).update({
            'record_update_time': datetime.now(timezone.utc).replace(tzinfo=None)
        })
        GlobalObjects.db_session.commit()
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),200

# 顯示垃圾桶中會議記錄
@bp.route('/trashcan_record', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def trashcan_record():
    response_object = {'status': 'success'}
    try:
        post_data = request.get_json()
        user = GlobalObjects.flask_auth.current_user()

        response_object["item"] = []
        record_get = (
            GlobalObjects.db_session.query(Record)
            .join(Project, Record.project_id == Project.id)
            .filter(Project.user_id==user.id, Project.id == post_data.get("project_id"))
            .filter(Record.record_trashcan == True)
            .order_by(desc(Record.record_creation_time))
            .all()
        )
        print("user_id: ", user.id)
        print("record_get: ", record_get)
        for records in record_get:
            tag_get = (GlobalObjects.db_session.query(Tag)
                       .join(TagTextBox, Tag.id == TagTextBox.tag_id)
                       .join(TextBox, TagTextBox.textBox_id == TextBox.id)
                       .join(Record, TextBox.record_id == Record.id)
                       .filter(TextBox.record_id == str(getattr(records, "id")))
                       .all()
                    )
            
            return_tags = []
            for tags in tag_get:
                return_tags.append(str(getattr(tags, "tag_name")))

            response_object["item"].append({'record_id':str(getattr(records, "id")),
                                            'record_name':str(getattr(records, "record_name")),
                                        #   'record_date':str(getattr(records, "record_date")),
                                        #   'record_department':str(getattr(records, "record_department")),
                                        #   'record_attendances':str(getattr(records, "record_attendances")),
                                        #   'record_place':str(getattr(records, "record_place")),
                                        #   'record_attendees_name':str(getattr(records,"record_attendees_name")),
                                        #   'record_host_name':str(getattr(records, "record_host_name")),
                                            'tags':return_tags
                                            })
        # data = (
        #     GlobalObjects.db_session.query(Record).filter(Record.project_id == post_data.get("project_id"), Record.record_trashcan==1, Record.user_id == user.id).all()
        # )
        # print(data)
        # response_object["item"] = [{"Record.id": row.id, "Record.project_id": row.project_id} for row in data]
        response_object["message"] = "垃圾桶顯示成功"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "垃圾桶顯示失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object)
    return jsonify(response_object)

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
    return jsonify(response_object),200

# 時間排序
@bp.route('/time_sort', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def time_sort():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    try:
        time_filter_unit = post_data.get("time_filter_unit")
        time_filter_length = int(post_data.get("time_filter_length")) if post_data.get("time_filter_length") else None
        time_sort = post_data.get("time_sort") if post_data.get("time_sort") else "asc"
        items = post_data.get("items")
        timestamp_name = post_data.get("timestamp_name")

        if time_filter_unit == "days":
            time_filter = datetime.now() - timedelta(days=time_filter_length)
        elif time_filter_unit == "months":
            time_filter = datetime.now() - timedelta(months=time_filter_length)
        elif time_filter_unit == "years":
            time_filter = datetime.now() - timedelta(years=time_filter_length)

        print(time_filter)

        # 使用 filter 函数过滤 items 列表
        filtered_items = list(
            filter(
                lambda item: datetime.fromisoformat(item[timestamp_name]) >= time_filter,
                items
            )
        )

        if time_sort == "desc":
            filtered_items = sorted(filtered_items, key=lambda x: datetime.fromisoformat(x[timestamp_name]), reverse=True)          
        elif time_sort == "asc":
            filtered_items = sorted(filtered_items, key=lambda x: datetime.fromisoformat(x[timestamp_name]))   

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        print(e)
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    response_object['items'] = filtered_items
    return jsonify(response_object),200

# 標籤搜尋
@bp.route('/tag_search', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
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

        # 計算事項與組別標籤符合數量
        event_and_group_tags = [tag_info["tag_name"] for tag_info in post_data.get("事項", [])] + [tag_info["tag_name"] for tag_info in post_data.get("組別", [])]
        tag_count_subquery = (
            GlobalObjects.db_session.query(
                TextBox.id.label("TextBox_id"),
                func.count(Tag.id).label("tag_count")
            )
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Tag.tag_name.in_(event_and_group_tags))
            .group_by(TextBox.id)
        ).subquery()
        
        textBox_query = (
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
                ).label("Tag"),
                TextBox.textBox_update_time
            )
            .select_from(User)
            .join(Project, User.id == Project.user_id)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .outerjoin(tag_count_subquery, TextBox.id == tag_count_subquery.c.TextBox_id)
            .filter(Project.id == id, Project.user_id == user.id)
        )

        # 搜尋符合日期標籤的 TextBox
        date_projects_query = (
            textBox_query.filter(Tag.tag_name.in_([tag_info["tag_name"] for tag_info in post_data.get("日期", [])]))
        )

        # 搜尋不符合日期標籤的 TextBox 或顯示沒有輸入日期標籤的情況
        undate_projects_query = (
            textBox_query.filter(
                ~exists()
                .where(and_(
                        Tag.tag_class == '日期',
                        Tag.tag_name.in_([tag_info["tag_name"] for tag_info in post_data.get("日期", [])]),
                        TagTextBox.textBox_id == TextBox.id
                ))
                .correlate_except(TextBox)
            )
        )

        date_projects_query = (
            date_projects_query.group_by(TextBox.id, TextBox.record_id, TextBox.textBox_content)
            .order_by(desc(func.coalesce(tag_count_subquery.c.tag_count, 0)))  # 按 tag 数量降序排序
        )
        undate_projects_query = (
            undate_projects_query.group_by(TextBox.id, TextBox.record_id, TextBox.textBox_content)
            .order_by(desc(func.coalesce(tag_count_subquery.c.tag_count, 0)))  # 按 tag 数量降序排序
        )

        date_projects_query = date_projects_query.order_by(desc(TextBox.textBox_update_time))
        undate_projects_query = undate_projects_query.order_by(desc(TextBox.textBox_update_time)) 

        date_projects = date_projects_query.all()
        undate_projects = undate_projects_query.all()

        response_object["item"] = {
            "date_match": [
                {
                    "TextBox_id": row[0],
                    "record_id": row[1],
                    "textBox_content": row[2],
                    "upload_time": row[4].isoformat(),
                    "Tag": json.loads(f"[{row[3]}]")
                }
                for row in date_projects
            ],
            "date_unmatch": [
                {
                    "TextBox_id": row[0],
                    "record_id": row[1],
                    "textBox_content": row[2],
                    "upload_time": row[4].isoformat(),
                    "Tag": json.loads(f"[{row[3]}]")
                }
                for row in undate_projects
                if row[0] not in [row[0] for row in date_projects]
            ]
        }
        print(response_object["item"])
        response_object["message"] = "標籤回傳成功"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "標籤回傳失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),200

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
        print(project_id)

        # 在porject_id已經篩過user_id了
        # tag = (
        #     GlobalObjects.db_session.query(Tag)
        #     .select_from(Project)
        #     .join(Record, Project.id == Record.project_id)
        #     .join(TextBox, Record.id == TextBox.record_id)
        #     .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
        #     .join(Tag, TagTextBox.tag_id == Tag.id)
        #     .filter(Project.id == project_id)
        #     .filter(Tag.tag_name == post_data.get("tag_name"))
        #     .first()
        # )

        # 原本的做法是搜尋"在這個project中，有沒有相同名稱的tag存在"。如果有就新增標籤。
        # 但我認為，這會少考慮到一個情況："將既存的標籤連結到新的textbox上"

        # 因此將程式邏輯改成：
        # if not "在這個project中存在這組tag-textBox relationship"
        #   if not "這個project中存在tag_name這個名字的標籤"
        #       新增一個tag到DB
        #   搜尋project中，相同tag_name的tag
        #   新增tag-textBox relationship到BD
        # else
        #   標籤已存在

        tag_textbox = (
            GlobalObjects.db_session.query(TagTextBox)
            .select_from(Project)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == project_id)
            .filter(TextBox.id == post_data.get("textBox_id"))
            .filter(Tag.tag_name == post_data.get("tag_name"))
            .scalar()
        )
        if tag_textbox is None:
            print("tag textbox relationship is none")
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
                print("The tag with tag_name is none")
                new_tag=Tag(tag_name=post_data.get("tag_name"), tag_class=post_data.get("tag_class"))
                GlobalObjects.db_session.add(new_tag)
                GlobalObjects.db_session.flush()
                GlobalObjects.db_session.commit()
                print("tag_name: ", post_data.get("tag_name"))
                # new_tagId = (
                #     GlobalObjects.db_session.query(Tag.id)
                #     .filter(Tag.tag_name == post_data.get("tag_name"))
                #     .first()
                # )

                # 這裡可能沒有考慮到"tag必須是這個project的tag"(因為不能改到其他project的tag，即使他們同名)
                # 所以直接拿剛創建的tag來用
                tag = new_tag

            print("Tag ID: ", tag.id)
            new_tagTextBox=TagTextBox(tag_id=tag.id, textBox_id=post_data.get("textBox_id"))
            GlobalObjects.db_session.add(new_tagTextBox)
            GlobalObjects.db_session.flush()
            GlobalObjects.db_session.commit()
            response_object["message"] = "新增{}成功".format(post_data.get("tag_name"))

            record_id = (
                GlobalObjects.db_session.query(Record.id)
                .join(TextBox, Record.id == TextBox.record_id)
                .filter(TextBox.id == textbox_id)
                .scalar()
            )
            GlobalObjects.db_session.query(Record).filter(Record.id == record_id,Record.user_id==user.id).update({
                'record_update_time': datetime.now(timezone.utc).replace(tzinfo=None)
            })
            GlobalObjects.db_session.commit()
        else:
            response_object["message"] = "標籤已存在"
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "新增失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object), 500
    return jsonify(response_object)

# 刪除標籤
@bp.route('/delete_tag', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def delete_tag():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    tag_id = post_data.get("tag_id")
    textBox_id = post_data.get("textBox_id")
    try:
        tag_textBox = GlobalObjects.db_session.query(TagTextBox).filter(TagTextBox.tag_id==tag_id, TagTextBox.textBox_id==textBox_id).first()
        print("tag_textBox relation to delete: ", tag_textBox)
        if tag_textBox is None:
            response_object["message"] = "標籤與文字方塊的關係不存在"
        else:
            # 把所有table連起來判斷user_id
            (project_id, record_id) = (
                GlobalObjects.db_session.query(Project.id, Record.id)
                .select_from(Project)
                .join(Record, Project.id == Record.project_id)
                .join(TextBox, Record.id == TextBox.record_id)
                .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
                .join(Tag, TagTextBox.tag_id == Tag.id)
                .filter(Tag.id == tag_id)
                .filter(TextBox.id == textBox_id)
                .filter(Project.user_id == user.id)
                .distinct()
                .first()
            )
            if project_id is None:
                response_object['message'] = "user不擁有此標籤，無法刪除"
                return jsonify(response_object),403

            GlobalObjects.db_session.query(TagTextBox).filter(TagTextBox.tag_id == tag_id, TagTextBox.textBox_id==textBox_id).delete()
            GlobalObjects.db_session.flush()

            tag_exist_in_tagTextBox = GlobalObjects.db_session.query(exists().where(TagTextBox.tag_id == tag_id)).scalar()
            if not tag_exist_in_tagTextBox:
                GlobalObjects.db_session.query(Tag).filter(Tag.id==tag_id).delete()
                GlobalObjects.db_session.flush()
                GlobalObjects.db_session.commit()
            response_object["message"] = "成功刪除標籤{}與文字方塊{}的連結".format(tag_id, textBox_id)
  
            GlobalObjects.db_session.query(Record).filter(Record.id == record_id,Record.user_id==user.id).update({
                'record_update_time': datetime.now(timezone.utc).replace(tzinfo=None)
            })
            GlobalObjects.db_session.commit()
    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = str(e)
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),500
    return jsonify(response_object),200

# 會議記錄搜尋 #順便船標籤
@bp.route('/search_records', methods=['POST'])
@GlobalObjects.flask_auth.login_required()
def search_records():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = GlobalObjects.flask_auth.current_user()
    search_term = post_data.get("search_term")
    try:
        record_name_get = (
            GlobalObjects.db_session.query(
                Record.id,
                Record.record_name,
                TextBox.textBox_content,
                func.locate(search_term, Record.record_name).label("search_term_locate"),
                Record.record_update_time
                )
            .join(Project, Record.project_id == Project.id)
            .join(TextBox, Record.id == TextBox.record_id)
            .filter(Project.user_id==user.id)
            .filter(Record.record_name.like(f"%{search_term}%"))
            .order_by(desc(Record.record_creation_time))
            .all()
        )

        record_content_get = (
            GlobalObjects.db_session.query(
                Record.id,
                Record.record_name,
                TextBox.textBox_content,
                # func.locate(search_term, TextBox.textBox_content).label("search_term_locate"),
                Record.record_update_time
                )
            .join(Project, Record.project_id == Project.id)
            .join(TextBox, Record.id == TextBox.record_id)
            .filter(Project.user_id==user.id)
            .filter(TextBox.textBox_content.like(f"%{search_term}%"))
            .order_by(desc(Record.record_creation_time))
            .all()
        )
        print(record_name_get)
        response_object["item"] = {
            "record_name": [],
            "record_content": []
        }

        for records in record_name_get:
            record_name_tag_get = (GlobalObjects.db_session.query(Tag)
                       .join(TagTextBox, Tag.id == TagTextBox.tag_id)
                       .join(TextBox, TagTextBox.textBox_id == TextBox.id)
                       .join(Record, TextBox.record_id == Record.id)
                       .filter(TextBox.record_id == str(getattr(records, "id")))
                       .all()
                    )
            
            record_name_return_tags = []
            for tags in record_name_tag_get:
                record_name_return_tags.append(str(getattr(tags, "tag_name")))

            response_object["item"]["record_name"].append(
                {
                    "record_id": records[0],
                    "record_name": records[1],
                    "textBox_content": records[2],
                    "search_term_locate": records[3]-1,
                    "record_update_time": records[4],
                    "tags": record_name_return_tags
                }
            ) 
        
        for records in record_content_get:

            content = records[2]
            positions = []
            start = 0
            while True:
                # 找到每一个符合的字符位置
                position = content.find(search_term, start)
                if position == -1:
                    break
                positions.append(position)
                start = position + 1  # 从下一个字符继续搜索

            record_content_tag_get = (GlobalObjects.db_session.query(Tag)
                       .join(TagTextBox, Tag.id == TagTextBox.tag_id)
                       .join(TextBox, TagTextBox.textBox_id == TextBox.id)
                       .join(Record, TextBox.record_id == Record.id)
                       .filter(TextBox.record_id == str(getattr(records, "id")))
                       .all()
                    )
        
            record_content_return_tags = []
            for tags in record_content_tag_get:
                record_content_return_tags.append(str(getattr(tags, "tag_name")))  

            response_object["item"]["record_content"].append(
                {
                    "record_id": records[0],
                    "record_name": records[1],
                    "textBox_content": records[2],
                    "search_term_locate": positions,
                    "record_update_time": records[3],
                    "tags": record_content_return_tags
                }
            ) 

    except Exception as e:
        response_object["status"] = "failed"
        response_object["message"] = "標籤尋找失敗"
        print(str(e))
        logging.exception('Error at %s', 'division', exc_info=e)
        GlobalObjects.db_session.rollback()
        return jsonify(response_object),500
    return jsonify(response_object),200