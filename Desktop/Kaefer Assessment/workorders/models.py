from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class ScaffoldComponent(models.Model):
    CATEGORY_CHOICES = [
        ('Tube', 'Tube'),
        ('Board', 'Board'),
        ('Coupler', 'Coupler'),
        ('Jack', 'Jack'),
        ('Frame', 'Frame'),
        ('Other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('NEW', 'NEW'),
        ('GOOD', 'GOOD'),
        ('REPAIR', 'REPAIR'),
        ('SCRAP', 'SCRAP'),
    ]

    SITE_CHOICES = [
        ('Secunda', 'Secunda'),
        ('Sasolburg', 'Sasolburg'),
    ]

    asset_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    length_mm = models.IntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='GOOD')
    site = models.CharField(max_length=100, choices=SITE_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    last_inspection = models.DateField(default=timezone.now)
    next_inspection = models.DateField()
    is_in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('asset_code', 'site')
        ordering = ['condition', 'name'] # Default order: condition asc, then name asc

    def clean(self):
        super().clean()
        if self.weight_kg is not None and self.weight_kg <= 0:
            raise ValidationError({'weight_kg': 'Weight (kg) must be greater than 0.'})
        
        if self.length_mm is not None and not (1 <= self.length_mm <= 6000):
            raise ValidationError({'length_mm': 'Length (mm) must be between 1 and 6000.'})

        if self.last_inspection and self.next_inspection and self.next_inspection < self.last_inspection:
            raise ValidationError({'next_inspection': 'Next inspection date must be on or after the last inspection date.'})

    def save(self, *args, **kwargs):
        self.full_clean() # Call full_clean to trigger model-level validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.asset_code}) - {self.site}"
