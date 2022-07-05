from django import forms

from myapp.models import Order


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 'YES'), (2, 'NO')])
    levels = forms.IntegerField(initial=1, min_value=1) 
    comments= forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")