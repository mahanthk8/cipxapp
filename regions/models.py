from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    regionId = models.CharField(max_length=6, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['regionId']),
        ]

    def __str__(self):
        return f"{self.name} ({self.regionId})"
