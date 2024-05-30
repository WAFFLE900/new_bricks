from flask import Blueprint, request, jsonify
from flask_app import GlobalObjects
from flask_app.models import *
from flask_app.auth import make_JWT, hash_password
from sqlalchemy.orm import *
from sqlalchemy import *
import logging

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
            session.query(Tag.tag_class, func.group_concat(func.DISTINCT(Tag.tag_name)).label('tag_names'))
            .select_from(Project)
            .join(Record, Project.id == Record.project_id)
            .join(TextBox, Record.id == TextBox.record_id)
            .join(TagTextBox, TextBox.id == TagTextBox.textBox_id)
            .join(Tag, TagTextBox.tag_id == Tag.id)
            .filter(Project.id == id, User.user_email == user.user_email)
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
        session.rollback()
        return jsonify(response_object),400
    return jsonify(response_object),400