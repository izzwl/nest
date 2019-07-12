import datetime
from django.db import models

class ActivityLog(models.Model):
    d_timestamp = models.DateTimeField(auto_now_add=True)
    c_nik = models.CharField(max_length=255)
    c_trx = models.CharField(max_length=255)
    c_func = models.CharField(max_length=255)
    c_key = models.CharField(max_length=255)

    def __str__(self):
        return self.d_timestamp.strftime("%d%b%y_%H:%m")+"-"+self.c_nik+"-"+self.c_trx+"-"+self.c_func
