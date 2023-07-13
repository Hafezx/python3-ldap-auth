# -*- coding: UTF-8 -*-
from flask import jsonify


def admin_panel_login_ms_health_check():
    return jsonify({"success": True})
