import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"


def get_env(var):
    return os.environ[var]


file_path = join(dirname(__file__), '.env')

dotenv_path = join(file_path)
if os.path.isfile(file_path):
    load_dotenv(file_path)

APP_LANG = get_env("APP_LANG")
DEBUG = get_env("DEBUG")
HOST = get_env("HOST")
PORT = get_env("PORT")


#login
AUTH_EXP_TIME = get_env("AUTH_EXP_TIME")
JWT_SECRET_KEY = get_env("JWT_SECRET_KEY")


#LDAP
LDAP_HOST = get_env("LDAP_HOST")
LDAP_PORT = get_env("LDAP_PORT")
LDAP_USER_SEARCH_FILTER = get_env("LDAP_USER_SEARCH_FILTER")
LDAP_BASE_DN = get_env("LDAP_BASE_DN")
LDAP_BIND_USER_DN = get_env("LDAP_BIND_USER_DN")
LDAP_BIND_USER_PASSWORD = get_env("LDAP_BIND_USER_PASSWORD")


# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Limiters
REQUEST_LIMIT = int(os.getenv("REQUEST_LIMIT",1))
REQUEST_LIMIT_TIME = os.getenv("REQUEST_LIMIT_TIME",'10m')

# logger
LOG_BASE_PATH = get_env("LOG_BASE_PATH")
LOGSTASH_HOST = get_env("LOGSTASH_HOST")
LOGSTASH_PORT = get_env("LOGSTASH_PORT")
USE_SELF_LOG_CONF = get_env("USE_SELF_LOG_CONF")
try:
    LOGGER_CONFIG_PATH = get_env("LOGGER_CONFIG_PATH")
    logger_conf_file = open(LOGGER_CONFIG_PATH + '/log_conf.json', 'r')
except Exception:
    logger_conf_file = open(os.path.dirname(os.path.abspath(__file__)) + '/log_conf.json', 'r')
LOGGER_CONFIG = json.loads(logger_conf_file.read())
