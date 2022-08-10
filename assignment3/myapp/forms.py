from django import forms

from myapp.models import Order, Student


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 'YES'), (2, 'NO')])
    levels = forms.IntegerField(initial=1, min_value=1) 
    comments= forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect(),
            'order_date': forms.SelectDateWidget()
        }


class ProfilePictureUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = Student
        fields = ['profile_picture', 'first_name', 'last_name', 'username']