from django.db import models
import pytz
from datetime import datetime
from django.utils import timezone

class BaseStockModel(models.Model):
    date = models.DateTimeField(null=True,blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    tick = models.CharField(max_length=20)
    timestamp = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True

import pytz

#set the timezone
tzInfo = pytz.timezone('Asia/Kolkata')

import calendar
import datetime

def to_local_datetime(utc_dt):
    """
    convert from utc datetime to a locally aware datetime according to the host timezone

    :param utc_dt: utc datetime
    :return: local timezone datetime
    """
    return datetime.datetime.fromtimestamp(calendar.timegm(utc_dt.timetuple()))



class CPSEETF(BaseStockModel):
    tick = models.CharField(max_length=20,default="CPSEETF")

    def save(self, *args, **kwargs):
        # Convert the timestamp to a datetime object
        utc_datetime = datetime.datetime.utcfromtimestamp(self.timestamp)
        
        # Define UTC timezone
        utc_timezone = pytz.timezone('UTC')
        
        # Make the datetime object timezone-aware
        utc_aware_datetime = utc_timezone.localize(utc_datetime)
        
        # Define IST timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        
        # Convert the datetime object to IST timezone
        ist_datetime = utc_aware_datetime.astimezone(ist_timezone)
        
        # Save the IST datetime to the model's date field
        self.date = ist_datetime
        
        super().save(*args, **kwargs)



    def __str__(self) -> str:
        return f"{self.date,self.tick}"
