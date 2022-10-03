from django.db import models


class Module(models.Model):  

    name = models.CharField(max_length=255, blank=True)
    access_level = models.IntegerField(default=1)

    
    def __str__(self):
        return self.name
