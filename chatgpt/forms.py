# chatgpt/forms.py
from django import forms

class DocumentUploadForm(forms.Form):
    csv_file = forms.FileField()
