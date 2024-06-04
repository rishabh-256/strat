# myapp/management/commands/my_command.py

from django.core.management.base import BaseCommand, CommandError


import datetime 
import pytz
import requests
from fake_useragent import UserAgent
from django.apps import apps

tick = "CPSEETF"


class Command(BaseCommand):
    help = 'Describe what your command does here'

    def handle(self, *args, **options):
        single_day_scrape(datetime.date(day=3,month=6,year=2024))



def scrape(tick,start_ts,end_ts,interval=1):
    ua = UserAgent(browsers=['edge', 'chrome','firefox'])
    header = {'User-Agent':str(ua.random)}
    interval=1
    url = f"https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/{tick}?endTimeInMillis={end_ts}&intervalInMinutes={interval}&startTimeInMillis={start_ts}"
    response = requests.get(url=url, headers=header)
    return response


"""
adding delayed means off the 5min regular time
"""

day_start = datetime.time(hour=0,minute=0,second=0)
day_close = datetime.time(hour=23, minute=59,second=59)

# for 1min interval, max 2 weeks data is supported, for 5min - 1month

def gen_ts(dt:datetime.datetime):
    ist = pytz.timezone('Asia/Kolkata')
    localized_datetime_object = ist.localize(dt)
    timestamp = int(localized_datetime_object.timestamp() * 1000)
    return timestamp     

def generate_timestamps_for_day(day:datetime.datetime):
    return [gen_ts(datetime.datetime.combine(day,time=day_start)),gen_ts(datetime.datetime.combine(day,time=day_close))]

import json

# Single day script
def single_day_scrape(day:datetime.date=datetime.datetime.today()):
    # By default it will scrape today's data
    start_ts, end_ts = generate_timestamps_for_day(day)
    response = scrape(tick=tick,start_ts=start_ts,end_ts=end_ts)
    response_dict = json.loads(response.text)
    grow_response_parser_to_save(data=response_dict,tick=tick)
    return True

def bi_weekly_scrape(start_date,end_date):
    pass

def long_date_range(start_date,end_date):
    pass

def get_model_by_name(app_label, model_name):
    try:
        model = apps.get_model(app_label, model_name)
        return model
    except LookupError:
        return None

def grow_response_parser_to_save(data,tick):
    for app_conf in apps.get_app_configs():
        try:
            model = app_conf.get_model(tick)
            break # stop as soon as it is found
        except LookupError:
            # no such model in this application
            pass

    for each in data["candles"]:
        model_object= model()
        model_object.timestamp = each[0]
        model_object.open = each[1]
        model_object.high = each[2]
        model_object.low = each[3]
        model_object.close = each[4]
        model_object.save()


# 1716349620,open=93.2,high=93.49,low=93.06,close=93.09,331366

