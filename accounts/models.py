# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta


class UserSecurity(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    SECURITY_QUESTIONS = [
        ('q1', 'What was your first pet\'s name?'),
        ('q2', 'What was your childhood nickname?'),
        ('q3', 'What is the name of your favorite teacher?'),
    ]

    question = models.CharField(
        max_length=2,
        choices=SECURITY_QUESTIONS,
        default='q1'
    )

    answer = models.CharField(max_length=255)
    answer_hash = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        import hashlib
        self.answer_hash = hashlib.sha256(
            self.answer.lower().strip().encode()
        ).hexdigest()
        super().save(*args, **kwargs)

    def verify_answer(self, user_answer):
        import hashlib
        user_hash = hashlib.sha256(
            user_answer.lower().strip().encode()
        ).hexdigest()
        return user_hash == self.answer_hash

    def __str__(self):
        return f"{self.user.username} - {self.get_question_display()}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_valid(self):
        return (not self.is_used and
                timezone.now() < self.expires_at)

    def __str__(self):
        return f"Token for {self.user.username}"