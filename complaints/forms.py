from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'complaint_image']

# Officer Update Form (For Updating Status, Adding Remarks and Resolution Image)
class OfficerUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'status',
            'remarks',
            'resolution_image'
        ]


from users.models import User

class ComplaintAssignForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['assigned_to', 'status', 'remarks']

    def __init__(self, *args, **kwargs):
        region = kwargs.pop('region', None)
        super().__init__(*args, **kwargs)

        if region:
            self.fields['assigned_to'].queryset = User.objects.filter(
                role='OFFICER',
                region=region,
                is_active=True
            )
