from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from processor.models import ProcessorUsage

class Tier(models.TextChoices):
    FREE = 'free', 'Free'
    BASIC = 'basic', 'Basic'
    PREMIUM = 'premium', 'Premium'


class TierLimits:
    LIMITS = {
        Tier.FREE: 2,  
        Tier.BASIC: 10, 
        Tier.PREMIUM: None
    }

    @classmethod
    def get_limit(cls, tier):
        return cls.LIMITS.get(tier)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, tier=Tier.FREE, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, tier=tier, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def has_reached_limit(self, user):
        limit = TierLimits.get_limit(user.tier)
        if limit is None:  
            return False
        today = timezone.now().date()
        usage_count = ProcessorUsage.objects.filter(user=user, timestamp__date=today).count()
        return usage_count >= limit


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    # Payment tier field
    tier = models.CharField(
        max_length=10,
        choices=Tier.choices,
        default=Tier.FREE,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"  # Field to be used for login
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]  # Fields required for user creation

    def __str__(self):
        return self.username

