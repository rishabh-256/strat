import datetime 
import pytz
import requests

tick = "CPSE"

def scrape(tick,start_ts,end_ts,interval=1):
    url = f"https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/{tick}?endTimeInMillis={end_ts}&intervalInMinutes={interval}&startTimeInMillis={start_ts}"
    print(url)
    response = requests.get("https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/CPSEETF?endTimeInMillis=1717024716248&intervalInMinutes=5&startTimeInMillis=1715365800000")
    return response


"""
adding delayed means off the 5min regular time
"""

market_opening_time = datetime.time(hour=9,minute=15)
market_closing_time = datetime.time(hour=15, minute=15)

# Single day script
# Weekly Script 
# Long term scrip

def timestamp_to_date_string(timestamp, date_format="%Y-%m-%d %H:%M:%S"):
    ist = pytz.timezone('Asia/Kolkata')
    date_object = datetime.fromtimestamp(timestamp, ist)
    date_string = date_object.strftime(date_format)
    return date_string


def gen_ts(dt:datetime.datetime):
    ist = pytz.timezone('Asia/Kolkata')
    localized_datetime_object = ist.localize(dt)
    timestamp = int(localized_datetime_object.timestamp() * 1000)
    return timestamp     


def generate_timestamps_for_day(day):
    return [gen_ts(datetime.datetime(year=2024,month=5,day=26,hour=0,minute=0,second=0)), gen_ts(datetime.datetime.now())]

def single_day_scrape():
    start_ts, end_ts = generate_timestamps_for_day(datetime.date(year=2024,month=5,day=29))
    [print(start_ts,end_ts)]
    res = scrape(tick=tick,start_ts=start_ts,end_ts=end_ts)
    print(res.content,res.status_code)

single_day_scrape()
