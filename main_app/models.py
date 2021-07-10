from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

DRINKS = (
    ('C', 'Coffee'),
    ('T', 'Tea'),
    ('W', 'Hot Water'),
    ('H', 'Hot Cocoa'),
    ('O', 'Other'),
)

TAGS = (
    ('DS', 'Dishwasher Safe'),
    ('HW', 'Hand Wash Only'),
    ('MS', 'Microwave Safe'),
    ('GH', 'Gets Hot in Microwave'),
    ('FR', 'Fragile'),
    ('MU', 'Metal'),
    ('MP', 'Multiple Pieces'),
    ('HL', 'Has Lid'),
)

class Instruction(models.Model):
    tag = models.CharField(
        max_length=2,
        choices=TAGS)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.get_tag_display()

    def get_absolute_url(self):
        return reverse('instructions_detail', kwargs={'pk': self.id})

class Mug(models.Model):
    name = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    instructions = models.ManyToManyField(Instruction)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'mug_id': self.id})

    def used_today(self):
        return self.use_set.filter(date=date.today()).count() > 0

class Photo(models.Model):
    url = models.CharField(max_length=200)
    mug = models.ForeignKey(Mug, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for mug_id: {self.mug_id} @{self.url}"

class Use(models.Model):
    date = models.DateField('use date')
    drink = models.CharField(
        max_length=1,
        choices=DRINKS,
        default=DRINKS[0][0]
        )
    mug = models.ForeignKey(Mug, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_drink_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']

