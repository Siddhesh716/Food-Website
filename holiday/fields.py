<<<<<<< HEAD
from django.db import models

class CustomTimeField(models.TimeField):
    def get_prep_value(self, value):
        if value is not None:
            return value.strftime('%H:%M:%S')
=======
from django.db import models

class CustomTimeField(models.TimeField):
    def get_prep_value(self, value):
        if value is not None:
            return value.strftime('%H:%M:%S')
>>>>>>> 591af9b (Initial commit)
        return value