from django.core.management.base import BaseCommand
from datetime import timedelta
import datetime 
import pytz
import requests
from fake_useragent import UserAgent
from django.apps import apps
import json

tick = "CPSEETF"


def ts_to_local_datetime(ts):
    utc_datetime = datetime.datetime.utcfromtimestamp(ts)
    india_timezone = pytz.timezone('Asia/Kolkata')
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(india_timezone)
    print(local_datetime)
    return local_datetime

class Command(BaseCommand):
    help = 'Describe what your command does here'

    def handle(self, *args, **options):
        single_day_scrape(tick="CPSEETF")

def scrape(tick,start_ts,end_ts,interval=1):
    ua = UserAgent(browsers=['edge', 'chrome','firefox'])
    header = {'User-Agent':str(ua.random)}
    interval=1
    url = f"https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/{tick}?endTimeInMillis={end_ts}&intervalInMinutes={interval}&startTimeInMillis={start_ts}"
    print("call being made")
    response = requests.get(url=url, headers=header)
    return response

"""
adding delayed means off the 5min regular time
"""

day_start = datetime.time(hour=0,minute=0,second=0)
day_end = datetime.time(hour=23, minute=59,second=59)

# for 1min interval, max 2 weeks data is supported, for 5min - 1month
def generate_timestamp(datetime):
        ist = pytz.timezone('Asia/Kolkata')
        localized_datetime_object = ist.localize(datetime)
        timestamp = int(localized_datetime_object.timestamp() * 1000)
        return timestamp

def generate_timestamps(date=False,range=False,opening_date=False,closing_date=False):    
    # it will take only date and will add opening and closing time depending on the params
    if date == range:
        raise Exception("Choose either date or date range")
    
    if date:
        opening_datetime = datetime.datetime.combine(date,time=day_start)
        closing_datetime = datetime.datetime.combine(date,time=day_end)
        return generate_timestamp(opening_datetime),generate_timestamp(closing_datetime)
    
    if range:
        if opening_date == closing_date:
            raise Exception(f"Invalid opening and closing date range: {opening_date, closing_date}")
        opening_datetime = datetime.datetime.combine(opening_date,time=day_start)
        closing_datetime = datetime.datetime.combine(closing_date,time=day_end)
        return generate_timestamp(opening_datetime),generate_timestamp(closing_datetime)


def generate_date_pairs(start_date, end_date):
    # List to store the date pairs
    date_pairs = []
    # Iterate over the range of dates
    current_start_date = start_date
    while current_start_date < end_date:
        current_end_date = current_start_date + timedelta(days=13)
        if current_end_date > end_date:
            current_end_date = end_date
        date_pairs.append((current_start_date, current_end_date))
        current_start_date = current_end_date + timedelta(days=1)
    return date_pairs

# Single day script
def single_day_scrape(tick,date:datetime.date=datetime.date.today()):
    # By default it will scrape today's data
    start_ts, end_ts = generate_timestamps(date=date)
    response = scrape(tick=tick,start_ts=start_ts,end_ts=end_ts)
    response = json.loads(response.text)
    grow_response_parser_to_save(data=response,tick=tick)
    return True

def date_range_scrape(start_date,end_date):
    pass
    if end_date < start_date or start_date == end_date:
        raise Exception('Invalid : date range')
    
    date_pairs = generate_date_pairs(start_date,end_date)
    
    for each in date_pairs:
        generate_timestamp(each)

from django.utils.timezone import make_aware

def grow_response_parser_to_save(data,tick):
    for app_conf in apps.get_app_configs():
        try:
            model = app_conf.get_model(tick)
            break # stop as soon as it is found
        except LookupError:
            # return print("No Model exist yet")
            pass

    for each in data["candles"]:
        model_object= model()
        model_object.timestamp = each[0]
        model_object.open = each[1]
        model_object.high = each[2]
        model_object.low = each[3]
        model_object.close = each[4]
        model_object.datetime = datetime.datetime.utcfromtimestamp((model_object.timestamp))
        model_object.save()