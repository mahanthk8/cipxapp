from django.db import models
from django.conf import settings
import random
import string

def generate_complaint_id(role_prefix):
    random_digits = ''.join(random.choices(string.digits, k=8))
    return f"CMP{role_prefix}{random_digits}"

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('SANITARY', 'Sanitary'),
        ('WATER', 'Water'),
        ('ELECTRICITY', 'Electricity'),
        ('FACILITY', 'New Facility'),
        ('CAMPAIGN', 'Campaign Request'),
        ('STALL', 'Stall Setup Request'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROCESS', 'In Process'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    complaintId = models.CharField(max_length=12, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Removed default=1 to prevent migration errors on empty databases
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.CASCADE,
        related_name='complaints',
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    action_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions'
    )

    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    complaint_image = models.ImageField(
        upload_to='complaints/',
        blank=True,
        null=True
    )

    resolution_image = models.ImageField(
        upload_to='resolutions/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        # Set region from user if not provided
        if not self.region and self.created_by:
            self.region = getattr(self.created_by, 'region', None)

        # Generate ID
        if not self.complaintId:
            role_prefix = 'C'
            if self.created_by.p_user:
                role_prefix = 'P'
            elif self.created_by.role == 'ADMIN':
                role_prefix = 'A'
            self.complaintId = generate_complaint_id(role_prefix)

        super().save(*args, **kwargs)
        
        # Log the action
        ComplaintAuditLog.objects.create(
            complaint=self,
            changed_by=self.action_by,
            change_description=f"Status: {self.status}, Assigned: {self.assigned_to}"
        )

    def __str__(self):
        return self.complaintId

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['region']),
        ]

class ComplaintAuditLog(models.Model):
    # Using string 'Complaint' avoids issues if classes move around
    complaint = models.ForeignKey(
        'Complaint', 
        on_delete=models.CASCADE, 
        related_name="audit_logs"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )
    change_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.complaint.complaintId} at {self.timestamp}"
