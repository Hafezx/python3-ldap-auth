import jwt
from flask import jsonify, Response, g, request
import json
import config
import redis


from flask import g
from ldap3 import Server, Connection, ALL

from app.logger import admin_panel_transaction_logger
from app.services.app_exceptions import InputValidationError, CustomException, AuthenticationException
from app.services.auth import authorize
from app.services.token_helper import generate_token
from app.services.aut_limiter import redis_limiter_check, redis_limiter_increase

from pprint import pprint
ACCESS_GROUP='CN={},OU={},OU=Users,OU=Groups,OU={},DC={},DC={}'

PERMISSION_ACCESS_GROUP = {
}


def auth_login_controller():
    log_action = "ADMIN_LOGIN"
    try:
        req_data = json.loads(request.data)
    except Exception as e:
        raise CustomException(' {}:درخواست نامعتبر است'.format(e), 406)

    if 'username' not in req_data or 'password' not in req_data:
        raise InputValidationError()
    username = req_data['username'].split('@')[0]
    password = req_data['password']


    redis_limiter_check(username)

    server = Server(host=config.LDAP_HOST, port=int(config.LDAP_PORT), get_info=ALL)
    try:
        conn = Connection(server, config.LDAP_BIND_USER_DN, config.LDAP_BIND_USER_PASSWORD, auto_bind=True)
    except Exception as e:
        raise CustomException("err{}".format(e), 406)

    if not conn.bind():
        raise CustomException('Failed to bind user', 406)

    # attributes = ['memberof']
    conn.search(search_base=config.LDAP_BASE_DN,
                search_filter='(&(objectClass=user)(sAMAccountName={}))'.format(username), attributes=['memberof'])

    if len(conn.entries) < 1:
        raise AuthenticationException()
    ldap_group = eval(conn.entries[0].entry_to_json())['attributes']['memberOf']
    user_groups = []
    for group in ldap_group:
        if group in PERMISSION_ACCESS_GROUP.keys():
            user_groups.append(PERMISSION_ACCESS_GROUP[group])

    print(user_groups)

    user_dn = eval(conn.entries[0].entry_to_json())['dn']
    if not conn.rebind(user_dn, password=password):
        admin_panel_transaction_logger(response_code=910201, action=log_action, username=username,
                                        log_message="User or pass is wrong")
        print("wrong pass")
        redis_limiter_increase(username)
        raise AuthenticationException()
    if ACCESS_GROUP not in ldap_group:
        admin_panel_transaction_logger(response_code=910201, action=log_action, username=username,
                                       log_message="User is not in admin panel group")
        raise AuthenticationException("User have not enough permissions to access admin panel")

    admin_panel_transaction_logger(response_code=910101, action=log_action, username=username,
                                      log_message="Successfully logged in with group {}".format(user_groups))
    g.user_group_in_login = user_groups




    return Response(
            response=json.dumps({"permissions": user_groups}),
            headers={'Authorization': "Bearer " + generate_token(user_groups, username)},
            mimetype='application/json',
            content_type='application/json'
            )


@authorize
def get_user_permission_list():
    user_token = g.get('user_token', None)
    if user_token:
        return jsonify({"permissions": user_token['user_groups']})

    return jsonify({"permissions": []})
