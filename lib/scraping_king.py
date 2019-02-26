import re
import sys
from os import environ
from datetime import datetime
from time import time

import requests
from sqlalchemy import desc

from lib.config_loader import config as conf
from .models.models import Event
from .models.models import Report
from .models.models import SubjectGroup
from .models.models import db


class ThiefKing(object):
    def __init__(self):
        self.session = self.__set_session()

    def get_report(self, id):
        item = db.query(Event).filter_by(id=id).first()

        return item

    def get_future_reports(self, limit=30):
        now = int(time())
        items = db.query(Event).order_by(
            Event.end).filter(Event.end > now).limit(limit).all()

        return items

    def get_joined_future_reports(self, limit=30):
        now = int(time())
        items = db.query(Report,
                         Event).join(Event, Report.TaskID == Event.id).filter(
                             Event.end > now).limit(limit).all()
        results = []
        for items in items:
            (report, event) = items
            dic = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'GroupName': report.GroupName,
                'start': event.start,
                'end': event.end,
                'startfortip': event.startfortip,
                'endfortip': event.endfortip,
                'allDay': event.allDay,
                'color': event.color,
                'isResubmit': report.IsResubmit,
                'PictureUrl': report.PictureUrl,
                'GroupID': report.GroupID
            }
            results.append(dic)

        return results

    def get_reports_tail(self, limit=20):
        joined = db.query(Report, SubjectGroup).join(
            SubjectGroup, Report.GroupID == SubjectGroup.Id).order_by(
                desc(Report.TaskID)).limit(limit).all()

        results = []
        for item in joined:
            r, s = item
            report = r.as_dict()
            subject = s.as_dict()
            report.update(s.as_dict())

            results.append(report)

        return results

    def get_joined_events(self, limit=30):
        items = db.query(Report).join(
            SubjectGroup, Report.GroupID == SubjectGroup.Id).join(
                Event, Report.TaskID == Event.id).all()
        return items

    def scraping_full_events_from_king(self):
        now = int(time())
        full_schedule_endpoint = conf.endpoint.get('fetchEvents')

        url = full_schedule_endpoint + str(now)
        json_data = self.session.get(url).json()

        print('save start..')
        regex = r'<.+?>'
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')

        results = []
        for e in json_data:
            (id, title, start, end, startfortip, endfortip, location,
             description, groupname, senderid, userid, allDay, color,
             textColor) = (e.get(k) for k in tuple(e.keys()))

            desc = re.sub(regex, '', description).translate(non_bmp_map)

            event = Event(
                id=id,
                title=title,
                start=start,
                end=end,
                startfortip=startfortip,
                endfortip=endfortip,
                location=location,
                description=desc,
                groupname=groupname,
                senderid=senderid,
                userid=userid,
                allDay=allDay,
                color=color,
                textColor=textColor)
            results.append(event)

            exists = db.query(
                Event.id).filter_by(id=e.get('id')).scalar() is None
            if exists:
                db.add(event)
                db.commit()
        print(f'saved {len(json_data)} Events\n')

        return results

    def scraping_groups_from_king(self):
        url = conf.endpoint.get('getGroups')
        json_data = self.session.get(url).json()

        results = []
        for items in json_data.values():
            for v in items:
                (Id, Name, Type, PictureUrl, Code, CodeEx, Year, HideStd,
                 UgrCodeEx, SyllPeriods,
                 Order) = (v.get(k) for k in tuple(v.keys()))

                subjectGroup = SubjectGroup(
                    Id=Id,
                    Code=Code,
                    CodeEx=CodeEx,
                    HideStd=HideStd,
                    Name=Name,
                    Order=Order,
                    PictureUrl=PictureUrl,
                    Type=Type,
                    Year=Year)
                results.append(subjectGroup)
                exists = db.query(
                    SubjectGroup.Id).filter_by(Id=v.get('Id')).scalar() is None
                if exists:
                    db.add(subjectGroup)
                    db.commit()

        return results

    def scraping_reports_from_king(self):
        url = conf.endpoint.get('getDeliverables')
        json_data = self.session.get(url).json()

        results = []
        for wrapper in json_data:
            for v in wrapper.get('Items'):
                (TaskID, TaskType, TaskKind, Title, DisplayDate, Status,
                 SubmissionEnd, GroupID, GroupName, PictureUrl,
                 IsResubmit) = (v.get(k) for k in tuple(v.keys()))
                report = Report(
                    TaskID=TaskID,
                    TaskType=TaskType,
                    TaskKind=TaskKind,
                    Title=Title,
                    DisplayDate=DisplayDate,
                    Status=Status,
                    SubmissionEnd=SubmissionEnd,
                    GroupID=GroupID,
                    GroupName=GroupName,
                    PictureUrl=PictureUrl,
                    IsResubmit=IsResubmit)
                exists = db.query(Report.TaskID).filter_by(
                    TaskID=v.get('TaskID')).scalar() is None
                results.append(report)
                if exists:
                    db.add(report)
                    db.commit()

        return results

    def scraping_content_alerts_from_king(self):
        url = conf.endpoint.get('getContentAlerts')
        json_data = self.session.get(url).json()
        results = []
        for v in json_data:
            (TaskID, Title, DisplayDate, GroupID, GroupName,
             TaskType) = (v.get(k) for k in tuple(v.keys()))
            content_alert = Report(
                TaskID=TaskID,
                Title=Title,
                DisplayDate=DisplayDate,
                GroupID=GroupID,
                GroupName=GroupName,
                TaskType=TaskType)
            exists = db.query(
                Report.TaskID).filter_by(TaskID=v.get('Id')).scalar() is None
            results.append(content_alert)
            if exists:
                db.add(content_alert)
                db.commit()

        return results

    def __set_session(self):
        session = requests.session()

        params = conf.login.get('params')

        payload = {
            'TextLoginID': environ.get('USER_ID'),
            'TextPassword': environ.get('PASSWORD'),
            '__EVENTVALIDATION': params.get('__EVENTVALIDATION'),
            '__VIEWSTATE': params.get('__VIEWSTATE'),
            '__VIEWSTATEGENERATOR': params.get('__VIEWSTATEGENERATOR'),
            'buttonHtmlLogon': params.get('buttonHtmlLogon')
        }

        url = conf.login.get('url')
        session.post(url=url, data=payload)

        return session
