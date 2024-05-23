from django.db import models
from django.contrib.auth.models import User
import random
# model for train addition
class Train(models.Model):
    train_name = models.CharField(max_length=100)
    train_no = models.CharField(max_length=20,  primary_key=True) 
     #unique=True,
    destination = models.CharField(max_length=100)
    origin_station = models.CharField(max_length=100)
    sleeper_seats = models.PositiveIntegerField(default=0)
    ac3_seats = models.PositiveIntegerField(default=0)
    ac2_seats = models.PositiveIntegerField(default=0)
    ac1_seats = models.PositiveIntegerField(default=0)
    sleeper_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ac3_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ac2_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ac1_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.train_name
    # model for ticket booking form

class Ticketghar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pnr_no = models.CharField(max_length=10, primary_key=True)
    train_name = models.CharField(max_length=100)
    train_no = models.CharField(max_length=20)
    destination = models.CharField(max_length=100)
    origin_station = models.CharField(max_length=100)
    train_class = models.CharField(max_length=50)
    copassengers = models.CharField(max_length=255)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    head = models.CharField(max_length=100)
    passage = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    train_date = models.DateField()

    def save(self, *args, **kwargs):
        # Generate a random 10-digit PNR number
        while True:
            random_pnr = ''.join(random.choices('0123456789', k=10))
            if not Ticketghar.objects.filter(pnr_no=random_pnr).exists():
                self.pnr_no = random_pnr
                break
        super(Ticketghar, self).save(*args, **kwargs)


    







