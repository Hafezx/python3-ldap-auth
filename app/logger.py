# -*- coding: UTF-8 -*-
import json
import socket
from flask import g
import datetime
from logging.config import dictConfig
import config
import logging
from flask import request

log_base_path = config.LOG_BASE_PATH
logging_dict = config.LOGGER_CONFIG
if config.USE_SELF_LOG_CONF == "1":
    dictConfig(logging_dict)
else:
    pass

app_logger = logging.getLogger('ms_logger')


def admin_panel_transaction_logger(response_code, action=None, username=None,
                            log_message=None, client_ip=None, **kwargs):
    app_logger.info(json.dumps({
        "logCode": response_code,
        "logMessage": log_message,
        'action': action,
        'username': username,
        'time': datetime.datetime.now().isoformat(),
        'clientIP': x_forwarded_for_ip_or_default() if client_ip is None else client_ip,
        'extra': kwargs
    }, separators=(',', ':')))


def ms_warning_logger(response_code, message=None, x_request_id=None, msisdn=None, action=None, host_name=None,
                      **kwargs):
    if msisdn is None:
        token_payload = g.get('token_payload', None)
        if token_payload:
            if "user_id" in token_payload:
                msisdn = token_payload["user_id"]

    app_logger.warning(json.dumps({
        "logCode": response_code,
        'XRequestID': g.get('request_id', None) if x_request_id is None else x_request_id,
        'logMessage': message,
        'msisdn': msisdn,
        'action': action,
        'time': datetime.datetime.now().isoformat(),
        'clientIP': x_forwarded_for_ip_or_default(),
        'hostName': socket.gethostname() if host_name is None else host_name,
        'extra': kwargs
    }, separators=(',', ':')))


def ms_error_logger(response_code, message=None, x_request_id=None, msisdn=None, action=None, host_name=None, **kwargs):
    if msisdn is None:
        token_payload = g.get('token_payload', None)
        if token_payload:
            if "user_id" in token_payload:
                msisdn = token_payload["user_id"]
    app_logger.error(json.dumps({
        "logCode": response_code,
        'XRequestID': g.get('request_id', None) if x_request_id is None else x_request_id,
        'logMessage': message,
        'msisdn': msisdn,
        'action': action,
        'time': datetime.datetime.now().isoformat(),
        'clientIP': x_forwarded_for_ip_or_default(),
        'hostName': socket.gethostname() if host_name is None else host_name,
        'extra': kwargs
    }, separators=(',', ':')))


def x_forwarded_for_ip_or_default():
    ip = request.headers.get('x-forwarded-for')
    if not validate_ip(ip):
        ip = request.remote_addr

    return ip


def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except Exception:
        return False
