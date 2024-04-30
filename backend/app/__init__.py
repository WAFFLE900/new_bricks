from dotenv import load_dotenv
from flask import Flask, current_app
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})
app.config['SECRET_KEY'] = 'secret'

#註冊個頁面 API 的 blueprint 至 app
from app.modules.login_register_module import login_register_module
app.register_blueprint(login_register_module)

from app.modules.personal_page_module import personal_page_module
app.register_blueprint(personal_page_module)

# 使用上下文管理器手動設置應用程式上下文
with app.app_context():
    current_app.config.from_object(__name__)
    
