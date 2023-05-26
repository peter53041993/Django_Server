from django.db import models

# Create your models here.

class ReportLog(models.Model):
    report_env = models.IntegerField()
    report_file = models.FilePathField()
    created = models.DateTimeField(auto_now_add=True)

