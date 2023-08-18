from django.db import models

class Train(models.Model):
    train_name = models.CharField(max_length=100)
    train_number = models.CharField(max_length=10)
    departure_time = models.TimeField()
    sleeper_available = models.PositiveIntegerField()
    ac_available = models.PositiveIntegerField()
    sleeper_price = models.DecimalField(max_digits=10, decimal_places=2)
    ac_price = models.DecimalField(max_digits=10, decimal_places=2)
    delayed_by = models.PositiveIntegerField()

    def __str__(self):
        return self.train_name
