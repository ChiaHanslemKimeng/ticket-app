from django import forms
from dashboardApp.models import Ticket, Review, profilemodel

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        widgets = {
            'description': forms.Textarea( attrs={'id': 'text_id'}),
            'title': forms.TextInput( attrs={'id': 'title_id'})
            }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES, attrs={'class': 'rate'}),
            'body': forms.Textarea(attrs={'class': 'bodyText'})
            }

class profilform(forms.ModelForm):
    class Meta:
        model=profilemodel
        fields=("image","gender")