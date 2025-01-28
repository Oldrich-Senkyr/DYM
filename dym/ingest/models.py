from django.db import models

# Create your models here.
from django.db import models

class IngestedData(models.Model):
    data = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IngestedData {self.id} at {self.received_at}"
