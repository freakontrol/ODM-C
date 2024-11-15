from django import forms
from .models import PartCategory, DocumentCategory

class PartCategoryForm(forms.ModelForm):
    class Meta:
        model = PartCategory
        fields = ['name', 'description']

class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description']