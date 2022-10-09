from django.db import models
from django.utils import timezone

class Module(models.Model):  

    name = models.CharField(max_length=255, blank=True)
    access_level = models.IntegerField(default=1)

    
    def __str__(self):
        return self.name


class News(models.Model):
    
    event = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    impact = models.CharField(max_length=255, blank=True, null=True)
    period = models.CharField(max_length=255, blank=True, null=True)
    actual = models.FloatField(max_length=255, blank=True, null=True)
    estimate = models.FloatField(max_length=255, blank=True, null=True)
    prev = models.FloatField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField('date', default='1700-01-01')
    time = models.TimeField('time', default='00:00:00')


    def get_minus(self):
        if self.actual and self.estimate:
            return round(self.actual - self.estimate, 1)
        else:
            return None

    def __str__(self):
        return str(self.event)


class ReferenceNews(models.Model):
    news_id = models.IntegerField()
    globalreport = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.news_id

