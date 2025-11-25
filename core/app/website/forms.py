from django import forms
from .models import Contact, ContactRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'number', 'message']

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = [
            "name",
            "number",
            "email",
            "city",
            "job",
            "capital",
            "message",
        ]