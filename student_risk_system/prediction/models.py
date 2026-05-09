from django.db import models

# Create your models here.

from django.db import models
import uuid
from django.contrib.auth.models import User

class StudentResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous_id = models.UUIDField(default=uuid.uuid4, editable=False)
    sleep_difficulty = models.IntegerField()
    wake_up = models.IntegerField()
    concentration = models.IntegerField()
    fatigue = models.IntegerField()
    skip_classes = models.IntegerField()
    caffeine = models.IntegerField()
    exercise = models.IntegerField()
    sleep_quality = models.IntegerField()
    stress = models.IntegerField()

    prediction = models.IntegerField()  # 0 or 1
    academic_performance = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anonymous_id = models.UUIDField(default=uuid.uuid4, editable=False)
    