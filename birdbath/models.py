from django.db import models


class Execution(models.Model):
    date_executed = models.DateTimeField(auto_now_add=True)
