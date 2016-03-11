from django.db import models


class Application(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    email = models.CharField(max_length=250)

    def __str__(self):
        return self.email

    class meta:
        ordering = ['create_date']
