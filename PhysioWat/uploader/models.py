from django.db import models


class Upload(models.Model):
    pic = models.FileField("CSV", upload_to="images/")
    upload_date=models.DateTimeField(auto_now_add =True)