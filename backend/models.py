from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, literal
from sqlalchemy.dialects.mysql import insert

db = SQLAlchemy()

class Delete(db.Model):
    __tablename__ = 'delete'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    delete_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Delete id={self.id} project_id={self.project_id} user_id={self.user_id} delete_date={self.delete_date}>'

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    groupMembers = db.relationship('GroupMember') 

    def __repr__(self):
        return f'<Group id={self.id} project_id={self.project_id}>'

class GroupMember(db.Model):
    __tablename__ = 'groups_member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_member_identity = db.Column(db.String(20), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    def __repr__(self):
        return f'<GroupMember id={self.id} user_id={self.user_id} group_member_identity={self.group_member_identity} group_id={self.group_id}>'

class Mention(db.Model):
    __tablename__ = 'mention'
    notification_id = db.Column(db.Integer, primary_key=True)
    notification_recipient_id = db.Column(db.Integer, nullable=False)
    notification_isRead = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Mention notification_id={self.notification_id} notification_recipient_id={self.notification_recipient_id} notification_isRead={self.notification_isRead}>'

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notification_content = db.Column(db.String(300), nullable=False)
    notification_sender_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Notification id={self.id} notification_content={self.notification_content} notification_sender_id={self.notification_sender_id}>'

class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    problem_content = db.Column(db.String(300), nullable=True)
    problem_solved = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Problem id={self.id} problem_content={self.problem_content} problem_solved={self.problem_solved} user_id={self.user_id}>'

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_type = db.Column(db.String(20), nullable=True)
    project_image = db.Column(db.String(20), nullable=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_trashcan = db.Column(db.Boolean, nullable=True)
    project_ended = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_edit = db.Column(db.Boolean, nullable=False)
    project_visible = db.Column(db.Boolean, nullable=False)
    project_comment = db.Column(db.Boolean, nullable=False)
    project_creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    project_edit_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Project id={self.id} project_name={self.project_name} user_id={self.user_id}>'

class ProjectSort(db.Model):
    __tablename__ = 'project_sort'
    type_id = db.Column(db.Integer, primary_key=True)
    project_type = db.Column(db.String(20), nullable=False)
    project_type_sort = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_ended = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<ProjectSort type_id={self.type_id} project_type={self.project_type} project_type_sort={self.project_type_sort} user_id={self.user_id} project_ended={self.project_ended}>'

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_date = db.Column(db.Date, nullable=True)
    record_department = db.Column(db.String(50), nullable=True)
    record_attendances = db.Column(db.Integer, nullable=True)
    record_place= db.Column(db.String(50), nullable=True)
    record_host_name = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_content = db.Column(db.String(100), nullable = True)
    search_time = db.Column(db.Date, nullable=True)

class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Tag id={self.id} tag_name={self.tag_name}>'

class TagTextBox(db.Model):
    __tablename__ = 'tag_textBox'

    tag_id = db.Column(db.Integer, primary_key=True)
    textBox_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Tag id={self.tag_id} textBox_id={self.textBox_id}>'

class TextBox(db.Model):
    __tablename__ = 'textBox'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    textBox_content = db.Column(db.String(300))
    record_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<TextBox id={self.id} textBox_content={self.textBox_content} record_id={self.record_id}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(64), unique=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(16), nullable=False)
    user_purpose = db.Column(db.String(10), nullable=True)
    user_identity = db.Column(db.String(10), nullable=True)
    user_otherTool = db.Column(db.String(100), nullable=True)
    user_avatar = db.Column(db.String(20), nullable=True)

    delete = db.relationship('Delete')
    groupMembers = db.relationship('GroupMember') 
    problem = db.relationship('Problem')
    project = db.relationship('Project')
    projectSort = db.relationship('ProjectSort')
    record = db.relationship('Record')
    searchHistory = db.relationship('SearchHistory')

    def __repr__(self):
        return f'<User id={self.id} user_email={self.user_email} user_name={self.user_name}>'
