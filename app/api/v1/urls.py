from app.api.v1 import api as api_v1
from app.api.v1.repositories.auth import auth_login_controller, get_user_permission_list

api_v1.add_url_rule('/admin/auth/login', view_func=auth_login_controller, methods=['POST'])
api_v1.add_url_rule('/admin/auth/user/permission', view_func=get_user_permission_list, methods=['GET'])
