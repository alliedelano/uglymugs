from django.forms import ModelForm
from .models import Use

class UseForm(ModelForm):
    class Meta:
        model = Use
        fields = ['date', 'drink']