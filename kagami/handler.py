import re
import datetime
from flask import session


def add_at(name: str):
    return '@' + name


def reply_handle(text: str, author_name: str):
    pattern = re.compile('(@[a-zA-Z_0-9]+)')
    matched = pattern.findall(text)
    if session.get('me') == author_name:
        ret = ''
    else:
        ret = '@' + author_name + ' '
    for x in matched:
        if x != add_at(session.get('me')) and x != add_at(author_name):
            ret += x + ' '
    return ret


def quote_handle(text: str, author_name: str):
    return 'RT @'+author_name+': '+text


def minutes_handle(status_time: datetime.datetime):
    now_time = datetime.datetime.utcnow()
    return str(int((now_time-status_time).seconds/60))


def date_handle(status_time: datetime.datetime):
    detail_time = status_time + datetime.timedelta(seconds=session.get('offset'))
    return detail_time.strftime("%Y-%m-%d %H:%M:%S")
