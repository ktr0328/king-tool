import json

from datetime import datetime, timedelta
from flask import Flask
from flask import Request
from flask import render_template
from flask_cors import CORS

from lib.config_loader import config as conf
from lib import scraping_king


def create_server():
    king = scraping_king.ThiefKing()

    king.scraping_groups_from_king()
    king.scraping_reports_from_king()
    king.scraping_content_alerts_from_king()

    reports = king.get_future_reports()
    if not reports:
        king.scraping_full_events_from_king()

    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['GET'])
    def top():
        reports = king.get_joined_future_reports()
        reports = [
            dict(dict(rest=get_diff_text(x.get('end'))), **x) for x in reports
        ]

        tail = [x for x in king.get_reports_tail()]
        conf_service = conf.service

        return render_template(
            'index.html', reports=reports, tail=tail, conf=conf_service)

    @app.route('/load_from_king', methods=['GET'])
    def load_from_king_lms():
        all_reports = [
            u.as_dict() for u in king.scraping_full_events_from_king()
        ]
        king.scraping_reports_from_king()
        king.scraping_content_alerts_from_king()

        return json.dumps(all_reports)

    @app.route('/reports', methods=['GET'])
    def get_future_reports():
        reports = [u.as_dict() for u in king.get_future_reports()]

        return json.dumps(reports)

    @app.route('/reports/<id>', methods=['GET'])
    def get_report(id):
        item = king.get_report(id)

        if item:
            return json.dumps(item.as_dict())
        else:
            return json.dumps({'result': 0})

    @app.route('/full_reports', methods=['GET'])
    def get_full_future_reports():
        results = king.get_joined_future_reports()

        return json.dumps(results)

    @app.route('/full_events', methods=['GET'])
    def get_full_events():
        events = [x.as_dict() for x in king.get_joined_events()]

        return json.dumps(events)

    return app


def get_diff_text(end_unix: int):
    end = datetime.fromtimestamp(end_unix)
    diff = end - datetime.now()
    diff_hours = diff.seconds // 3600
    diff_minutes = (diff.seconds // 60) % 60

    rest = f'あと{diff.days}日'
    if diff_hours <= 1:
        rest = f'あと{diff_minutes}分'
    if diff.days <= 0:
        rest = f'あと{diff_hours}時間'

    return rest
