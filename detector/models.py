from django.db import models
from django.contrib.auth.models import User


class GenderDetectionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gender_results')
    form1_result = models.CharField(max_length=255, blank=True)
    form2_result = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Gender Detection Result"
        verbose_name_plural = "Gender Detection Results"

    def __str__(self):
        return f"{self.user.username} - Gender Detection ({self.created_at})"
