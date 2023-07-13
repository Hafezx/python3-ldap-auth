import codecs
import json
import os

import config


def get_message(code, lang=config.APP_LANG):
    error_list = codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/../assets/lang.json', 'rb')
    error_list = json.loads(error_list.read())

    if lang not in error_list or code not in error_list[lang]:
        return "Error Message Not Found"

    return error_list[lang][code]


class CustomException(Exception):
    """ Default Status Code : 422 - Unprocessable Entity"""
    status_code = 422

    def __init__(self, message, error_code=-1, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.code = error_code
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        response = {'message': self.message, 'resultCode': self.code}
        return response


class HMACException(CustomException):
    def to_dict(self):
        response = {'message': self.message, 'code': self.code, 'status': 'error'}
        return response


# Auth Exceptions


class AuthenticationException(CustomException):
    def __init__(self, message=get_message('40101')):
        CustomException.__init__(self, message, error_code=40101, status_code=401)


class AuthenticationIPLimited(CustomException):
    def __init__(self, message=get_message('40102')):
        CustomException.__init__(self, message, error_code=40102, status_code=401)


class AuthenticationExpiredTokenException(CustomException):
    def __init__(self, message=get_message('40103')):
        CustomException.__init__(self, message, error_code=40103, status_code=401)


class PermissionDeniedException(CustomException):
    def __init__(self, message=get_message('0101')):
        CustomException.__init__(self, message, error_code=101, status_code=403)


# Inputs

class InputValidationError(CustomException):
    def __init__(self, message=get_message('1001')):
        CustomException.__init__(self, message, error_code=1001, status_code=422)


class XMLParseError(CustomException):
    def __init__(self, message=get_message('1004')):
        CustomException.__init__(self, message, error_code=1004, status_code=422)


class UnknownError(CustomException):
    def __init__(self, message=get_message('1002')):
        CustomException.__init__(self, message, error_code=1002, status_code=422)


class ConnetionError(CustomException):
    def __init__(self, message=get_message('1003')):
        CustomException.__init__(self, message, error_code=1003, status_code=422)


class FormNotFound(CustomException):
    def __init__(self, message=get_message('1005')):
        CustomException.__init__(self, message, error_code=1005, status_code=404)


class ProvideAllFields(CustomException):
    def __init__(self, message=get_message('1006')):
        CustomException.__init__(self, message, error_code=1006, status_code=422)

# Rate Limit
class RateLimitException(CustomException):
    def __init__(self, message=get_message('1007')):
        CustomException.__init__(self, message, error_code=1007, status_code=429)
