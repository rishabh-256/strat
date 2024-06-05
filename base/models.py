from django.db import models

class BaseStockModel(models.Model):
    timestamp = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField(null=True,blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    tick = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.datetime.astimezone()}"

class CPSEETF(BaseStockModel):
    tick = models.CharField(max_length=20,default="CPSEETF")