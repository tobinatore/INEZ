from django.db import models
import datetime

class Grocery_List(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.datetime.now)
    price = models.FloatField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=500)
    search = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date', 'title']

    class Admin:
        pass
