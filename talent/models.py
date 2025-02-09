from django.db import models
from django.contrib.auth.models import User

class TalentProfile(models.Model):
    ROLES = [
        ('TALENT', 'Talent'),
        ('CASTING', 'Casting Professional'),
        ('ADMIN', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    portfolio = models.URLField(blank=True, null=True)
    bio = models.TextField()
    skills = models.CharField(max_length=200)
    is_minor = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLES, default='TALENT')

    def __str__(self):
        return self.full_name

class ParentalConsent(models.Model):
    talent = models.OneToOneField(TalentProfile, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    consent_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Consent for {self.talent.full_name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Subscription(models.Model):
    PLANS = [
        ('SIX_MONTHS', 'Six Months - $550 + GST'),
        ('ONE_YEAR', 'One Year - $800 + GST'),
        ('LIFETIME', 'Lifetime - $3500 + GST'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLANS)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

class PayPerView(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    video_url = models.URLField()

    def __str__(self):
        return self.title