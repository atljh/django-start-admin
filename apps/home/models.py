from django.db import models


class Modul(models.Model):  

    name = models.CharField(max_length=255, blank=True)
    access_level = models.IntegerField(default=1)


    def __str__(self):
        return self.name


# class News(models.Model):
