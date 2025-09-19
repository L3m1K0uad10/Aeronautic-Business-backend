from django.db import models



class Consultation(models.Model):
    CONSULTATION_TYPES = [
        ('type1', 'General Inquiry'),
        ('type2', 'Technical Support'),
        ('type3', 'Aviation Investment Advisory'),
        ('type4', 'Making business with us'),
        ('type5', 'conferences and events'),
        ('type6', 'Other'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.consultation_type} on {self.date} at {self.time}"